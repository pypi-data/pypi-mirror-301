import brevitas.nn as qnn
from brevitas_examples.common.generative.quantizers import IntWeightSymmetricGroupQuant
from brevitas_examples.llm.llm_quant.export import export_packed_onnx
import torch.nn as nn
import torch


class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = qnn.QuantLinear(32, 32, weight_quant=IntWeightSymmetricGroupQuant, weight_bit_width=4, weight_group_size=8)

    def forward(self, x):
        return self.linear(x)

model = Model()
model(torch.randn(1, 32))
model.eval()
export_packed_onnx(model, torch.randn(1,32), 'test.onnx')


# from functools import partial
# shape_dict = dict()
# def hook(module, input, output, name):
#     shape_dict[id(module)] = output.shape

# hook_list = []
# for name, module in pipe.unet.named_modules():
#     if isinstance(module, (torch.nn.Linear, torch.nn.Conv2d)):
#         partial_hook = partial(hook, name=name)
#         hook_list.append(module.register_forward_hook(partial_hook))

# ### FORWARD CALL HERE
# pipe(prompt, ...)
# ### END FORWARD CALL

# for name, shape in shape_dict.items():
#     print(name, shape)