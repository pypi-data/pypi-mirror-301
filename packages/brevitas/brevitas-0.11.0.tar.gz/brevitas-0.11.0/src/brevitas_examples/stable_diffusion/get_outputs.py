# Copyright 2024 Advanced Micro Devices, Inc
#
# Licensed under the Apache License v2.0 with LLVM Exceptions.
# See https://llvm.org/LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

from pathlib import Path

import torch

from shark_turbine import aot

from ..model import Unet2DConditionModel, ClassifierFreeGuidanceUnetModel




def main():
    from ....utils import cli

    parser = cli.create_parser()
    cli.add_input_dataset_options(parser)
    parser.add_argument("--device", default="cuda:0", help="Torch device to run on")
    parser.add_argument("--dtype", default="float16", help="DType to run in")
    parser.add_argument("--export", type=Path, help="Export to path (vs run)")
    parser.add_argument(
        "--inputs",
        type=Path,
        help="Safetensors file of inputs (or random if not given)",
    )
    args = cli.parse(parser)

    device = args.device
    dtype = getattr(torch, args.dtype)

    ds = cli.get_input_dataset(args)
    ds.to(device=device)

    cond_unet = Unet2DConditionModel.from_dataset(ds)
    mdl = ClassifierFreeGuidanceUnetModel(cond_unet)

    # Run a step for debugging.
    if args.inputs:
        inputs = load_inputs(args.inputs, dtype=dtype, device=device)
    else:
        inputs = get_random_inputs(dtype=dtype, device=device)

    if args.export:
        # Temporary: Need a dedicated exporter.
        output = aot.export(
            mdl,
            kwargs=inputs,
        )
        output.save_mlir(args.export)
    else:
        results = mdl.forward(**inputs)
        print("1-step results:", results)


if __name__ == "__main__":
    main()