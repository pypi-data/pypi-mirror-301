from dependencies import value, this
from brevitas.core.quant.int import RescalingIntQuant
from brevitas.core.restrict_val import QuantRestrictValue
from brevitas.core.stats.stats_wrapper import SCALAR_SHAPE
from brevitas.inject.enum import ScalingPerOutputType
from brevitas.quant.scaled_int import Int8WeightPerTensorFloat
import brevitas.nn as qnn
import torch


class QuantScalingInt(Int8WeightPerTensorFloat):
    bit_width=8
    module = (this<<1).module
    tracked_parameter_list = (this<<1).tracked_parameter_list
    upstream_scaling = (this<<1).scaling_per_output_type
    rescaling_int_quant = RescalingIntQuant

    @value
    def scaling_shape(scaling_per_output,scaling_per_output_channel_shape, expanded_groupwise_shape, group_dim, upstream_scaling):
        if scaling_per_output == ScalingPerOutputType.TENSOR:
            scaling = SCALAR_SHAPE
        elif scaling_per_output == ScalingPerOutputType.CHANNEL:
            scaling = scaling_per_output_channel_shape
        elif scaling_per_output == ScalingPerOutputType.GROUP:
            # Scaling shape is like expanded_groupwise_shape but has 1 in position group_dim + 1
            assert expanded_groupwise_shape is not None, "Per Group scaling not correctly configured"
            assert group_dim is not None, "Per Group scaling not correctly configured"
            size = list(expanded_groupwise_shape)
            size[group_dim + 1] = 1
            scaling = tuple(size)
        
        # When quantizing scale of groupwise, there will be one extra dim compared to the normal case
        if upstream_scaling == ScalingPerOutputType.GROUP:
            scaling = list(scaling)
            scaling.insert(-1, 1)
            scaling = tuple(scaling)
        return scaling
    

class QuantScaleInt8WeightPerTensorFloat(Int8WeightPerTensorFloat):
    scaling_int_quant = QuantScalingInt
    restrict_scaling_impl = QuantRestrictValue
    scaling_per_output_type = ScalingPerOutputType.CHANNEL
    group_size=32 

    @value
    def restrict_value_float_to_int_impl():
        return this.scaling_int_quant.rescaling_int_quant

linear = qnn.QuantLinear(64, 768, weight_quant=QuantScaleInt8WeightPerTensorFloat)
o = linear(torch.randn(1, 64))
print("----------------")
print(torch.max(torch.abs(linear.weight - linear.quant_weight().value)))





# class QuantScalingInt(SolveStatsReduceDimFromEnum,
#                         SolveWeightScalingStatsInputDimsFromModule,
#                         SolveScalingStatsInputViewShapeImplFromEnum,
#                         SolveScalingStatsOpFromEnum,
#                         SolveBitWidthImplFromEnum,
#                         SolveTensorQuantFloatToIntImplFromEnum,
#                         SolveRestrictScalingImplFromEnum,
#                         SolveIntScalingImplFromEnum,
#                         SolveParameterScalingImplFromEnum,
#                         SolveParameterTensorClampImplFromEnum,
#                         SolveParameterScalingInitFromEnum,
#                         SolveParameterScalingShape,
#                         SolveWeightScalingPerOutputChannelShapeFromModule,
#                         SolveWeightTensorQuantFromEnum,
#                         SolveDtypeDeviceFromTrackedParameterList,
#                         SolveInputViewImpl):
#     scaling_int_quant = None
#     rescaling_int_quant = RescalingIntQuant
#     quant_type = QuantType.INT
#     bit_width_impl_type = BitWidthImplType.CONST
#     float_to_int_impl_type = FloatToIntImplType.ROUND
#     narrow_range = True
#     signed = True
#     zero_point_impl = ZeroZeroPoint
#     scaling_impl_type = ScalingImplType.STATS
#     scaling_stats_op = StatsOp.MAX
#     scaling_min_val = 1e-10
#     scaling_per_output_type = ScalingPerOutputType.CHANNEL
#     restrict_scaling_type = RestrictValueType.FP
#     bit_width = 8
#     module = (this<<1).module
#     tracked_parameter_list = (this<<1).tracked_parameter_list
#     upstream_scaling = (this<<1).scaling_per_output_type

#     @value
#     def scaling_shape(scaling_per_output,scaling_per_output_channel_shape, expanded_groupwise_shape, group_dim, upstream_scaling):
#         if scaling_per_output == ScalingPerOutputType.TENSOR:
#             scaling = SCALAR_SHAPE
#         elif scaling_per_output == ScalingPerOutputType.CHANNEL:
#             scaling = scaling_per_output_channel_shape
#         elif scaling_per_output == ScalingPerOutputType.GROUP:
#             # Scaling shape is like expanded_groupwise_shape but has 1 in position group_dim + 1
#             assert expanded_groupwise_shape is not None, "Per Group scaling not correctly configured"
#             assert group_dim is not None, "Per Group scaling not correctly configured"
#             size = list(expanded_groupwise_shape)
#             size[group_dim + 1] = 1
#             scaling = tuple(size)
#         if upstream_scaling == ScalingPerOutputType.GROUP:
#             scaling = list(scaling)
#             scaling.insert(-1, 1)
#             scaling = tuple(scaling)
#         return scaling
    