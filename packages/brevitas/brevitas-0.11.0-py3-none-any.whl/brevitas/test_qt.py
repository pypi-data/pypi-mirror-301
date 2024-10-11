import brevitas.nn as qnn
import torch
from tqdm import tqdm


class UInt4Tensor(torch.Tensor):
    @staticmethod
    def __new__(cls, elem, **kwargs):
        assert elem.dtype is torch.uint8
        assert not kwargs.get("requires_grad", False)
        kwargs["requires_grad"] = False
        return torch.Tensor._make_wrapper_subclass(
            cls, elem.shape, dtype=torch.uint8, **kwargs
        )

    def __init__(self, elem, **kwargs):
        self.elem = elem
    @classmethod
    def from_unpacked(cls, unpacked):
        uint5 = UInt4Tensor(unpacked)
        print(uint5)
        return uint5


    def __tensor_flatten__(self):
        return ["elem"], None

    @staticmethod
    def __tensor_unflatten__(flattened, meta, outer_size, outer_stride):
        assert meta is None
        elem = flattened["elem"]
        return UInt4Tensor(elem)
    __torch_function__ = torch._C._disabled_torch_function_impl


class PerChannelSymmetricWeightUInt4Tensor(UInt4Tensor):
    @staticmethod
    def __new__(cls, elem, scales, **kwargs):
        return super().__new__(cls, elem, **kwargs)

    def __init__(self, elem, scales, **kwargs):
        super().__init__(elem, **kwargs)

        self.scales = scales

    def __tensor_flatten__(self):
        return ["elem", "scales"], None
    @classmethod
    def __torch_dispatch__(cls, func, types, args, kwargs=None):
        return super().__torch_dispatch__(func, types, args, kwargs)
    @staticmethod
    def __tensor_unflatten__(flattened, meta, outer_size, outer_stride):
        assert meta is None
        elem = flattened["elem"]
        scales = flattened["scales"]
        return PerChannelSymmetricWeightUInt4Tensor(elem, scales)
    @classmethod
    def from_unpacked(cls, unpacked, scales):
        return cls(unpacked, scales)

    @classmethod
    def from_float(cls, w_fp32):
        quant = PerChannelSymmetricWeightUInt4Tensor.from_unpacked(
            unpacked=w_fp32, scales=torch.randn(1)
        )

        return quant
c = PerChannelSymmetricWeightUInt4Tensor.from_float(torch.tensor([0, 5, 1, 3], dtype=torch.uint8))

print(c)
raise

print("Start")
a = qnn.QuantIdentity()
params = list(a.parameters())
opt = torch.optim.SGD(a.parameters())
for _ in tqdm(range(500)):
    o = a(torch.randn(1, 3))
    loss = o.mean()
    loss.backward()
    if _ == 400:
        print(params[0].grad)
        raise
    opt.step()