from typing import Optional

import torch
from torch import Tensor, nn
from torch.autograd import grad
from torch.nn import functional as F

from adv_lib.utils.visdom_logger import VisdomLogger


def bp(model: nn.Module,
       inputs: Tensor,
       labels: Tensor,
       targeted: bool = False,
       num_steps: int = 100,
       γ: float = 0.7,
       α: float = 2,
       levels: Optional[int] = 256,
       callback: Optional[VisdomLogger] = None) -> Tensor:
    """
    Boundary Projection (BP) attack from https://arxiv.org/abs/1912.02153.

    Parameters
    ----------
    model : nn.Module
        Model to attack.
    inputs : Tensor
        Inputs to attack. Should be in [0, 1].
    labels : Tensor
        Labels corresponding to the inputs if untargeted, else target labels.
    targeted : bool
        Whether to perform a targeted attack or not.
    num_steps : int
        Number of optimization steps.
    γ : float
        Factor by which the norm will be modified. new_norm = norm * (1 + or - γ).
    levels : int
        If not None, the returned adversarials will have quantized values to the specified number of levels.
    callback : Optional

    Returns
    -------
    adv_inputs : Tensor
        Modified inputs to be adversarial to the model.

    """
    if inputs.min() < 0 or inputs.max() > 1: raise ValueError('Input values should be in the [0, 1] range.')
    device = inputs.device
    batch_size = len(inputs)
    batch_view = lambda tensor: tensor.view(batch_size, *[1] * (inputs.ndim - 1))

    # Init variables
    multiplier = 1 if targeted else -1
    δ = torch.zeros_like(inputs, requires_grad=True)

    # Init trackers
    best_l2 = torch.full((batch_size,), float('inf'), device=device)
    best_adv = inputs.clone()
    adv_found = torch.zeros(batch_size, dtype=torch.bool, device=device)

    for i in range(num_steps):
        adv_inputs = inputs + δ
        logits = model(adv_inputs)

        if i == 0:
            num_classes = logits.shape[1]
            one_hot_labels = F.one_hot(labels, num_classes=num_classes)

        # "softmax_cross_entropy_better" loss
        tmp = one_hot_labels * logits
        logits_1 = logits - tmp
        j_best = logits_1.amax(dim=1)
        logits_2 = logits_1 - j_best.unsqueeze(1) + one_hot_labels * j_best.unsqueeze(1)
        tmp_s = tmp.amax(dim=1)
        up = tmp_s - j_best
        down = logits_2.exp().add(1).sum(dim=1).log()
        loss = up - down

        g = grad(multiplier * loss.sum(), δ, only_inputs=True)[0]
        d = inputs - adv_inputs.detach()  # N x C x H x W

        snd = d.flatten(1).norm(p=2, dim=1).clamp_(min=1e-6)  # N
        nd = d / batch_view(snd)  # N x C x H x W

        sng = g.flatten(1).norm(p=2, dim=1).clamp_(min=1e-6)  # N
        ng = g / batch_view(sng)  # \hat{g} - shape: N x C x H x W

        cos_ψ = (nd * ng).flatten(1).sum(dim=1)  # r - shape: N
        sin_ψ = (1 - cos_ψ ** 2).sqrt()  # N

        pred_labels = logits.argmax(1)
        is_adv = (pred_labels == labels) if targeted else (pred_labels != labels)
        is_smaller = snd < best_l2
        is_both = is_adv & is_smaller
        adv_found.logical_or_(is_adv)
        best_l2 = torch.where(is_both, snd, best_l2)
        best_adv = torch.where(batch_view(is_both), adv_inputs.detach(), best_adv)

        if callback is not None:
            callback.accumulate_line('loss', i, loss.mean(), title='BP - Loss')
            callback_best = best_l2.masked_select(adv_found).mean()
            callback.accumulate_line(['l2', 'best_l2'], i, [snd.mean(), callback_best])
            callback.accumulate_line(['success'], i, [adv_found.float().mean()], title='BP - ASR')

            if (i + 1) % (num_steps // 20) == 0 or (i + 1) == num_steps:
                callback.update_lines()

        # step-size decay
        ε = γ + i * (1 - γ) / (num_steps + 1)

        # search
        p_search = α * ε * ng

        # refine step
        # out
        λ = (d * ng).flatten(1).sum(dim=1)
        g_ort = d - batch_view(λ) * ng
        ε_out = snd * ε

        # estimate β out LS
        dis = snd * ε  # N
        ngo = g_ort.flatten(1).norm(p=2, dim=1).clamp_(min=1e-6)  # N
        g_ort_ = g_ort / batch_view(ngo)  # N x C x H x W
        tmp = (d * g_ort_).flatten(1).sum(dim=1)  # N
        an_tmp = batch_view(tmp.square()) - d.square() + batch_view(dis)  # N x C x H x W
        min_β = batch_view(tmp) - an_tmp.sqrt()  # N x C x H x W
        max_β = batch_view(tmp)  # N x C x H x W

        p_min = min_β * g_ort_  # N x C x H x W
        p_max = max_β * g_ort_  # N x C x H x W
        DMin = (d - p_min).mul_(levels - 1).round_().div_(levels - 1).flatten(1).norm(p=2, dim=1)
        DMax = (d - p_max).mul_(levels - 1).round_().div_(levels - 1).flatten(1).norm(p=2, dim=1)
        for j in range(7):
            β = (min_β + max_β) / 2
            p = β * g_ort_
            D = (d - p).mul_(levels - 1).round_().div_(levels - 1).flatten(1).norm(p=2, dim=1)
            flag = D < dis
            DMin = torch.where(flag, D, DMin)
            DMax = torch.where(flag, DMax, D)
            min_β = torch.where(batch_view(flag), β, min_β)
            max_β = torch.where(batch_view(flag), max_β, β)
        dMin = (DMin - dis).abs_()
        dMax = (DMax - dis).abs_()
        flag = dMax < dMin
        β = torch.where(batch_view(flag), max_β, min_β)

        # out_p
        μ = (batch_view(sin_ψ * snd) / β - 1).clamp_(min=0)
        p_out = g_ort / (1 + μ)

        # estimate β in simple
        dis = snd / ε
        ngo, g_ort_ = sng, ng
        p_o = (d * g_ort_).flatten(1).sum(dim=1)  # N
        bac = dis.square() - snd.square() + p_o.square()  # N
        β = p_o + bac.sqrt()
        β_min = torch.full_like(dis, 0.1)
        β.clamp_(min=β_min)

        p_in = ng * batch_view(β)

        delta = torch.where(batch_view(adv_found), p_in, p_search)
        delta = torch.where(batch_view(is_adv), p_out, delta)

        adv_x = (adv_inputs + delta).clamp_(min=0, max=1)
        adv_x.mul_(levels - 1).round_().div_(levels - 1)

        δ.data = adv_x - inputs

    return best_adv
