from brevitas.graph.calibrate import inference_mode
import brevitas.nn as qnn
from brevitas.quant.scaled_int import Int8ActPerTensorFloat
import torch
import torch.nn as nn

class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = qnn.QuantLinear(3, 8, input_quant=Int8ActPerTensorFloat)
    
    def forward(self, x):
        return self.linear(x)
    

model = Model()
model.cuda()
model.eval()
input = torch.randn(1, 3, device='cuda')
with torch.no_grad(), inference_mode(model):
    model(input)
model = torch.compile(model)
with torch.no_grad():
    o = model(input)
def hook(*args, **kwargs):
    print("Oh")

model.register_forward_hook(hook)

print(o)