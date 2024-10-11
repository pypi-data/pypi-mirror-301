import torch
import torch.nn as nn

import brevitas.nn as qnn
from brevitas.quant import Int8WeightPerTensorFloat, Int8WeightPerTensorFloatMSE
from brevitas.core.scaling import ScalingImplType

torch.manual_seed(0)

class WQMSE(Int8WeightPerTensorFloatMSE):
    bit_width=8
    #scaling_impl_type=ScalingImplType.PARAMETER_FROM_STATS

class WQ(Int8WeightPerTensorFloat):
    bit_width=8
    #scaling_impl_type=ScalingImplType.PARAMETER_FROM_STATS

with torch.no_grad():
    in_features = 16
    out_features = 32
    batch_size = 100

    x = 2*torch.rand((batch_size,in_features)) - 1.
    l = nn.Linear(in_features, out_features)
    l.eval()
    y = l(x)

    #ql = qnn.QuantLinear(in_features, out_features, weight_quant=WQ) # l2_err = 0.0054
    ql = qnn.QuantLinear(in_features, out_features, weight_quant=WQMSE) # l2_err = 298.4549
    ql.train()
    ql(x)
    ql.load_state_dict(l.state_dict(), strict=False)
    ql.eval()
    qy = ql(x)
    print(ql.quant_weight().scale)

    l2_err = ((y - qy)**2).sum()
    print(l2_err)