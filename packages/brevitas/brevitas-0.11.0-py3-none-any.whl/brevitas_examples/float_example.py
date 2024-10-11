import brevitas.nn as qnn
from brevitas.quant.experimental.float_quant_ocp import Fp8e5m2OCPWeight
from brevitas.quant.experimental.float_quant_ocp import Fp8e5m2OCPAct
from brevitas.quant.experimental.float_quant_ocp import Fp8e4m3OCPWeight
from brevitas.quant.experimental.float_quant_ocp import Fp8e4m3OCPAct

float8_conv = qnn.QuantConv2d(3, 8, weight_quant=Fp8e5m2OCPWeight, input_quant=Fp8e5m2OCPAct)