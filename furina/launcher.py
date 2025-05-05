# -*- coding: utf-8 -*-
import os
from .engine import llama_cpp
from .lib import path

def run_server(port: int, model_name: str, quantization: str='',
               force_cpu_only=None, fource_gpu_type=None):
    # Calculate the model paths.
    model_name: str = model_name.lower()
    if len(quantization) > 0:
        model_name += "_" + quantization
    model_path: str = os.path.join(path.PATH_ASSERT_MODEL, f"{model_name}.gguf")
    # Check whether the model exists.
    if not os.path.isfile(model_path):
        # Download the model.
        pass
    llama_cpp.run_server(port, model_path,
                         force_cpu_only=force_cpu_only,
                         fource_gpu_type=fource_gpu_type)
