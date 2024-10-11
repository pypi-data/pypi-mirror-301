import copy
import gc
import logging
from typing import Any, Dict, List, Optional

import model_compressor_impl as _impl
import torch

logger = logging.getLogger("ptq_auto_optimization")

__all__ = [
    "ptq_auto_optimize",
]


def ptq_auto_optimize(
    model,
    calib_dataloader,
    valid_func,
    data_preprocessor,
    weight_dtype,
    weight_nbits,
    act_dtype,
    act_nbits,
    bn_folding=True,
    qlevel=1,
    target_machine='RGDA0',
    qlevel3_emul_mode='normal',
    disable_inout=(False, False),
    concrete_args: Optional[Dict[str, Any]] = None,
    skipped_methods: List[str] = None,
):
    return _impl.ptq_auto_optimize(
        model,
        calib_dataloader,
        valid_func,
        data_preprocessor,
        weight_dtype,
        weight_nbits,
        act_dtype,
        act_nbits,
        bn_folding=bn_folding,
        qlevel=qlevel,
        target_machine=target_machine,
        qlevel3_emul_mode=qlevel3_emul_mode,
        disable_inout=disable_inout,
        concrete_args=concrete_args,
        skipped_methods=skipped_methods,
    )


def find_optimial_pts_quant_scheme(
    model,
    calib_loader,
    valid_func,
    data_preprocessor,
    weight_dtype,
    weight_nbits,
    act_dtype,
    act_nbits,
    bn_folding=True,
    qlevel=1,
    target_machine='RGDA0',
    qlevel3_emul_mode='normal',
    disable_inout=(False, False),
    concrete_args: Optional[Dict[str, Any]] = None,
    skipped_methods: List[str] = None,
):
    return _impl.find_optimial_pts_quant_scheme(
        model,
        calib_loader,
        valid_func,
        data_preprocessor,
        weight_dtype,
        weight_nbits,
        act_dtype,
        act_nbits,
        bn_folding,
        qlevel,
        target_machine,
        qlevel3_emul_mode,
        disable_inout,
        concrete_args,
        skipped_methods,
    )


def find_optimal_pch_quant_scheme(
    model,
    calib_loader,
    valid_func,
    best_pts_weight_method,
    best_pts_act_method,
    pts_percentile,
    data_preprocessor,
    weight_dtype,
    weight_nbits,
    act_dtype,
    act_nbits,
    bn_folding=True,
    qlevel=1,
    target_machine='RGDA0',
    qlevel3_emul_mode='normal',
    disable_inout=(False, False),
    concrete_args: Optional[Dict[str, Any]] = None,
    skipped_methods: List[str] = None,
):
    return _impl.find_optimal_pch_quant_scheme(
        model,
        calib_loader,
        valid_func,
        best_pts_weight_method,
        best_pts_act_method,
        pts_percentile,
        data_preprocessor,
        weight_dtype,
        weight_nbits,
        act_dtype,
        act_nbits,
        bn_folding,
        qlevel,
        target_machine,
        qlevel3_emul_mode,
        disable_inout,
        concrete_args,
        skipped_methods,
    )


def reset_quantizer(quant_model):
    return _impl.reset_quantizer(quant_model)


def change_descript_perch_quantizer(quant_model, weight_calib_method, act_calib_method):
    return _impl.change_descript_perch_quantizer(quant_model, weight_calib_method, act_calib_method)
