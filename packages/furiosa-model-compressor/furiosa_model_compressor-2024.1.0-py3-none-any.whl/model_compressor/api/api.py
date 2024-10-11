from functools import wraps
import inspect
import logging
import os
from pathlib import Path
import sys
import types
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
import traceback
import sys
import model_compressor_impl as _impl
import torch
from torch import fx

from . import ptq_auto_optimization

logger = logging.getLogger("api")

MAP_LOCATION = Optional[
    Union[Callable[[torch.Tensor, str], torch.Tensor], torch.device, str, Dict[str, str]]
]

__all__ = [
    "create_quantsim_model",
    "calibrate",
    "export",
    "save_tracing_guide",
    "create_pipeline_parallelism_model",
    "load_on_multi_gpus_from_cpu",
    # e2e_verfication
    "set_model_to_dump_golden_model",
    "enable_qlv4_skip_output_rounding",
    "check_conformance",
    # immigrate_qparam 사용하는 경우를 위해서 추가됨. API정리 후 한번에 깔끔히 제거 필요합니다.
    # https://github.com/furiosa-ai/model-compressor-private/pull/697
    "save_qformat_qparam",
    # NOTE: 아래 함수들은 모두 제거해도 되지 않을까요?
    "load",
    "save_qformat",
    # "ptq_auto_optimize",
    "extract_qformat_and_qparam",
]


def track_kwargs(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 현재 함수에 대한 인수 정보를 가져옴
        sig = inspect.signature(func)
        bound_args = sig.bind_partial(*args, **kwargs).arguments

        # 사용자가 명시적으로 제공한 인수를 추적
        wrapper._user_provided_args = set(kwargs.keys()).union(bound_args.keys())

        return func(*args, **kwargs)

    wrapper._user_provided_args = set()
    return wrapper


@track_kwargs
def create_quantsim_model(
    model: torch.nn.Module,
    output_path: str = './',
    weight_calib_method: str = "AMAX_SYM",
    weight_dtype: str = "int8",
    weight_granularity: str = "channel",
    weight_nbits: int = 8,
    act_calib_method: str = "PERCENTILE_ASYM",
    act_dtype: str = "int8",
    act_granularity: str = "channel",
    act_nbits: int = 8,
    qformat_path: Union[str, dict, None] = None,
    qparam_path: Union[str, dict, None] = None,
    bn_folding: bool = True,
    outlier_percentile: Optional[int] = None,
    outlier_dtype: str = "int8",
    outlier_nbits: int = 8,
    act_zp_equalizing: str = 'disabled',
    qlevel: int = 1,
    target_machine: str = 'RGDA0',
    qlevel3_emul_mode: str = 'normal',
    weighted_op_emul_dtype: str = 'fp64',
    nodes_excluded_from_outlier_compensation: List[str] = None,
    disable_inout: Tuple[bool, bool] = (False, False),
    dataloader: Optional[torch.utils.data.DataLoader] = None,
    data_preprocessor: Optional[Callable] = None,
    concrete_args: Optional[Dict[str, Any]] = None,
    skipped_methods: List[str] = None,
    bcq_iter: int = 10,
    kv_dtype: str = 'bf16',
    decode_phase: bool = False,
    quantized_prefill_model: fx.GraphModule = None,
    draw_each_trs_graph=False,
    delete_org_weight=False,  # True일 때 문제가 되는 상황이 있는지?
    immigrate_qparams=False,
    unify_inter_pipeline_dtype=True,
    set_pow_dtype_to_bf16=False,
    debug_mode_force_to_int8=False,
    transformer_block_yaml=None,
    disable_old_node_mapping=False,
    disable_auto_node_mapping=False,
    v_cache_granularity: str = 'channel',
) -> fx.GraphModule:
    try:
        return _impl.api.api.create_quantsim_model(
            model,
            output_path=output_path,
            weight_calib_method=weight_calib_method,
            weight_dtype=weight_dtype,
            weight_granularity=weight_granularity,
            weight_nbits=weight_nbits,
            act_calib_method=act_calib_method,
            act_dtype=act_dtype,
            act_granularity=act_granularity,
            act_nbits=act_nbits,
            qformat_path=qformat_path,
            qparam_path=qparam_path,
            bn_folding=bn_folding,
            outlier_percentile=outlier_percentile,
            outlier_dtype=outlier_dtype,
            outlier_nbits=outlier_nbits,
            act_zp_equalizing=act_zp_equalizing,
            qlevel=qlevel,
            target_machine=target_machine,
            qlevel3_emul_mode=qlevel3_emul_mode,
            weighted_op_emul_dtype=weighted_op_emul_dtype,
            nodes_excluded_from_outlier_compensation=nodes_excluded_from_outlier_compensation,
            disable_inout=disable_inout,
            dataloader=dataloader,
            data_preprocessor=data_preprocessor,
            concrete_args=concrete_args,
            skipped_methods=skipped_methods,
            bcq_iter=bcq_iter,
            kv_dtype=kv_dtype,
            decode_phase=decode_phase,
            quantized_prefill_model=quantized_prefill_model,
            draw_each_trs_graph=draw_each_trs_graph,
            delete_org_weight=delete_org_weight,
            immigrate_qparams=immigrate_qparams,
            unify_inter_pipeline_dtype=unify_inter_pipeline_dtype,
            set_pow_dtype_to_bf16=set_pow_dtype_to_bf16,
            debug_mode_force_to_int8=debug_mode_force_to_int8,
            transformer_block_yaml=transformer_block_yaml,
            disable_old_node_mapping=disable_old_node_mapping,
            disable_auto_node_mapping=disable_auto_node_mapping,
            v_cache_granularity=v_cache_granularity,
        )
        
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print("Error Occurred:", exc_value)
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        raise


def export(
    model: fx.GraphModule,
    exported_model_name: str = 'exported_model.bin',
    output_path: str = './',
    target_machine: str = 'RGDA0',
    quantized_prefill_model: fx.GraphModule = None,
    transformer_block_yaml: Optional[Path] = None,
    disable_old_node_mapping=False,
):
    """qlevel4단계의 quantized model weight를 저장.

    Args:
        model (fx.GraphModule): MCM IR을 포함한 fx graph module.
        file_path (str)
        qparam_path (str)
        qformat_path (str)
        target_machine (str, optional):Defaults to 'RGDA0'.
    """
    return _impl.api.api.export(
        model,
        exported_model_name,
        output_path,
        target_machine,
        quantized_prefill_model,
        transformer_block_yaml,
        disable_old_node_mapping,
    )


def load(quantized_model: fx.GraphModule, file_path: str, map_location: MAP_LOCATION = None):
    """Load weight to quantized model."""
    _impl.api.api.load(quantized_model, file_path, map_location)
    return


def extract_qformat_and_qparam(
    model: fx.GraphModule = None,
):
    return _impl.api.api.extract_qformat_and_qparam(model)


def save_qformat(
    model: fx.GraphModule = None,
    qformat_dict: Optional[dict] = None,
    qformat_out_path: Optional[str] = None,
    weight_calib_method: Optional[str] = None,
    weight_granularity: Optional[str] = None,
    weight_dtype: Optional[str] = None,
    act_calib_method: Optional[str] = None,
    act_granularity: Optional[str] = None,
    act_dtype: Optional[str] = None,
    kv_dtype: Optional[str] = None,
    disable_mods: Optional[List[str]] = None,
    disable_inout: Tuple[bool, bool] = (False, False),
    v_cache_granularity: Optional[str] = None,
) -> None:
    _impl.api.api.save_qformat(
        model,
        qformat_dict,
        qformat_out_path,
        weight_calib_method,
        weight_granularity,
        weight_dtype,
        act_calib_method,
        act_granularity,
        act_dtype,
        kv_dtype,
        disable_mods,
        disable_inout,
        v_cache_granularity,
    )
    return


def save_qformat_qparam(
    model: fx.GraphModule = None,
    qformat_dict: Optional[dict] = None,
    qformat_out_path: Optional[str] = None,
    qparam_dict: Optional[dict] = None,
    qparam_out_path: Optional[str] = None,
    weight_calib_method: Optional[str] = None,
    weight_granularity: Optional[str] = None,
    weight_dtype: Optional[str] = None,
    act_calib_method: Optional[str] = None,
    act_granularity: Optional[str] = None,
    act_dtype: Optional[str] = None,
    kv_dtype: Optional[str] = None,
    disable_mods: Optional[List[str]] = None,
    disable_inout: Tuple[bool, bool] = (False, False),
    v_cache_granularity: Optional[str] = None,
) -> None:
    _impl.save_qformat_qparam(
        model,
        qformat_dict,
        qformat_out_path,
        qparam_dict,
        qparam_out_path,
        weight_calib_method,
        weight_granularity,
        weight_dtype,
        act_calib_method,
        act_granularity,
        act_dtype,
        kv_dtype,
        disable_mods,
        disable_inout,
        v_cache_granularity,
    )


@track_kwargs
def calibrate(
    model: fx.GraphModule,
    dataloader: Optional[torch.utils.data.DataLoader],
    model_name: str = None,
    weight_calib_method: str = "AMAX_SYM",
    weight_dtype: str = "int8",
    weight_granularity: str = "channel",
    weight_nbits: int = 8,
    act_calib_method: str = "PERCENTILE_ASYM",
    act_dtype: str = "int8",
    act_granularity: str = "channel",
    act_nbits: int = 8,
    group_size: Optional[int] = None,
    percentile: float = 99.9,
    is_dynamic_quant: bool = False,
    act_zp_equalizing: str = 'disabled',
    autoscale: str = 'disabled',
    autoscale_calib_method: str = 'auto',
    autoscale_calib_kwargs: Optional[Dict] = None,
    autoclip: bool = False,
    outlier_calib_cfg: Optional[Dict] = None,
    ckpt_folder_path: Optional[Path] = None,
    target_machine: str = 'gpu',
    disable_mods: Optional[List[str]] = None,
    data_preprocessor: Optional[Callable] = None,
    model_type: Optional[str] = None,
    transformer_block_yaml: Optional[Path] = None,
    smoothquant_alpha: float = 0.5,
    nodes_excluded_from_auto_scale_calib: Optional[List] = None,
    nodes_excluded_from_auto_clip_calib: Optional[List] = None,
    unify_smooth_factor: bool = False,
    module_name_to_replace_smooth_factor: Optional[str] = None,
    module_name_for_smooth_factor: Optional[str] = None,
    outlier_percentile: Optional[int] = None,
    output_path: str = './',
    kv_dtype: Optional[str] = None,
    disable_inout: Tuple[bool, bool] = (False, False),
    enable_multi_gpu: bool = False,
    memory_saving_mode: bool = False,
    v_cache_granularity: str = 'channel',
) -> None:
    return _impl.api.api.calibrate(
        model,
        dataloader=dataloader,
        model_name=model_name,
        weight_calib_method=weight_calib_method,
        weight_dtype=weight_dtype,
        weight_granularity=weight_granularity,
        weight_nbits=weight_nbits,
        act_calib_method=act_calib_method,
        act_dtype=act_dtype,
        act_granularity=act_granularity,
        act_nbits=act_nbits,
        group_size=group_size,
        percentile=percentile,
        is_dynamic_quant=is_dynamic_quant,
        act_zp_equalizing=act_zp_equalizing,
        autoscale=autoscale,
        autoscale_calib_method=autoscale_calib_method,
        autoscale_calib_kwargs=autoscale_calib_kwargs,
        autoclip=autoclip,
        outlier_calib_cfg=outlier_calib_cfg,
        ckpt_folder_path=ckpt_folder_path,
        target_machine=target_machine,
        disable_mods=disable_mods,
        data_preprocessor=data_preprocessor,
        model_type=model_type,
        transformer_block_yaml=transformer_block_yaml,
        smoothquant_alpha=smoothquant_alpha,
        nodes_excluded_from_auto_scale_calib=nodes_excluded_from_auto_scale_calib,
        nodes_excluded_from_auto_clip_calib=nodes_excluded_from_auto_clip_calib,
        unify_smooth_factor=unify_smooth_factor,
        module_name_to_replace_smooth_factor=module_name_to_replace_smooth_factor,
        module_name_for_smooth_factor=module_name_for_smooth_factor,
        outlier_percentile=outlier_percentile,
        output_path=output_path,
        kv_dtype=kv_dtype,
        disable_inout=disable_inout,
        enable_multi_gpu=enable_multi_gpu,
        memory_saving_mode=memory_saving_mode,
        v_cache_granularity=v_cache_granularity,
    )


def load_on_multi_gpus_from_cpu(model: fx.GraphModule) -> fx.GraphModule:
    return _impl.api.api.multi_chip.load_on_multi_gpus_from_cpu(model)


def create_pipeline_parallelism_model(
    model: fx.GraphModule,
    ckpt_folder_path: str,
    subgraph_ir: str = 'fx_graph',
    shared_param_dict: Optional[Dict] = None,
):
    return _impl.api.api.create_pipeline_parallelism_model(
        model,
        ckpt_folder_path,
        subgraph_ir,
        shared_param_dict,
    )


def save_tracing_guide(
    model: fx.GraphModule,
    trace_guide_json_path: str,
):
    '''
    model fx.graph에서 trasnformer block들을 찾아서 json파일로 저장합니다.
    '''

    _impl.api.api.save_tracing_guide(model, trace_guide_json_path)


def set_model_to_dump_golden_model(
    dump_file_path,
    model: fx.GraphModule,
    dumping_range: str = 'qlv4_linear',
    dumping_mode: str = 'only-in-out',
    qlv4_skip_output_rounding: bool = False,
    dumping_before_rounding: bool = False,
    dump_in_append_mode: bool = False,
):
    _impl.api.api.set_model_to_dump_golden_model(
        dump_file_path,
        model,
        dumping_range=dumping_range,
        dumping_mode=dumping_mode,
        qlv4_skip_output_rounding=qlv4_skip_output_rounding,
        dumping_before_rounding=dumping_before_rounding,
        dump_in_append_mode=dump_in_append_mode,
    )


def enable_qlv4_skip_output_rounding(model: fx.GraphModule, applied_range: str = 'linear'):
    _impl.api.api.enable_qlv4_skip_output_rounding(model, applied_range)


def check_conformance(
    comparison_model: Union[fx.GraphModule, str],
    golden_file_path: str,
    dumping_range: str = 'qlv4_linear',
    result_file_path: Optional[str] = None,
    mcm_name_to_check: Optional[str] = None,
    mcm_name_map: Optional[dict] = None,
    compare_rounded_result: bool = False,
):
    """
    주어진 모델과 골든 모델 결과를 비교하는 함수를 실행합니다.

    Args:
        comparison_model(fx.GraphModule or str): MCM으로 변환된 테스트 모델 또는 모델 dump file path
        golden_file_path (str]): 골든 모델 결과를 포함하고 있는 파일 경로.
        dumping_range (str, optional): Test를 진행할 layer 범위 설정. 기본값은 'qlv4_linear'입니다.
        result_file_path (Optional[str], optional): 비교 결과를 저장할 파일 경로.
            지정되지 않을 경우, 현재 시간 정보를 기준으로 파일 이름이 설정됩니다. 기본값은 None입니다.
        mcm_name_to_check (Optional[str], optional): 특정 레이어만 비교할 경우, 설정이 필요한 변수로 테스트를 수행할 모듈 이름을 설정합니다. 기본값은 None입니다.
        mcm_name_map (Optional[dict], optional): 골든 모델과 현재 모델의 레이어 이름이 일치하지 않을 경우,
            {현재_모델_레이어_이름: 골든_모델_레이어_이름} 형식의 매핑 정보를 입력합니다. 기본값은 None입니다.
        compare_rounded_result (bool, optional): 비교할 값을 반올림 전 혹은 후로 할지 설정합니다.
            True로 설정하면 rounding 후로 비교하고, False로 설정하면 rounding 전으로 비교합니다. 기본값은 False입니다.
    """
    _impl.api.api.check_conformance(
        comparison_model,
        golden_file_path,
        dumping_range=dumping_range,
        result_file_path=result_file_path,
        mcm_name_to_check=mcm_name_to_check,
        mcm_name_map=mcm_name_map,
        compare_rounded_result=compare_rounded_result,
    )
