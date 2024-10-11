from typing import NamedTuple
from brevitas.quant_tensor.int_quant_tensor import IntQuantTensor
import torch

# Remove the bases check
def is_namedtuple_cls_patched(cls): 
    """Test if an object is a namedtuple or a (torch.return_types|torch.autograd.forward_ad).* quasi-namedtuple""" 
    try: 
        if issubclass(cls, tuple): 
            module = getattr(cls, "__module__", None) 
            return module in ("torch.return_types", "torch.autograd.forward_ad") or ( 
                hasattr(cls, "_make") and hasattr(cls, "_fields") 
            )
    except TypeError:
        pass
    return False

# Not the prettiest but it does the job
torch._dynamo.utils.is_namedtuple_cls.__code__ = is_namedtuple_cls_patched.__code__

torch._dynamo.allow_in_graph
def create_nt(a1, a2):
    return BaseDtype(a1, a2)

class BaseDtype(NamedTuple):
    a: torch.Tensor
    b: torch.Tensor

    def __add__(self, other):
        return create_nt(self.a + other.a, self.b + other.b)
    @classmethod
    def __torch_function__(cls, func, types, args=(), kwargs=None):
        args = (args[0].a)
        return func(args)

class MyDType(BaseDtype):

    def __new__(cls, a, b):
        # This is needed to do type checking on init variables
        return super().__new__(cls, a, b)

    def __add__(self, other):
        return MyDType(self.a + other.a, self.b)

    @classmethod
    def __torch_function__(cls, func, types, args=(), kwargs=None):
        args = (args[0].a)
        return func(args)

# This is required to create MyDType within the forward pass
# Removing __new__ and inheriting directly from NamedTuple seems to work but it does not fit my use case
# torch._dynamo.allow_in_graph(MyDType)



class Model(torch.nn.Module):
  def __init__(self):
    super().__init__()
    
  def forward(self, a1, a2):
    inp1 = create_nt(a1, a2)
    inp2 = create_nt(a1, a2)
    return torch.nn.functional.relu(inp1 + inp2)


model = Model()
non_compiled_output = model(torch.tensor(3.), torch.tensor(0.))
print(f"Correct output: {non_compiled_output}")
model = torch.compile(model, fullgraph=True)
compiled_output = model(torch.tensor(3.), torch.tensor(0.))
# Correct output: MyDType(a=tensor(6.), b=tensor(0.))
print(f"Less correct output: {compiled_output}")
# Less correct output: (tensor(3.), tensor(0.), tensor(3.), tensor(0.))