# -*- coding: utf-8 -*-
import os
from .engine import llama_cpp
from .lib import model

def run_server(port: int, model_name: str, num_of_params: str = '', quantization: str='',
               force_cpu_only=None, fource_gpu_type=None):
    # Calculate the model paths.
    local_model_path: str = model.get_local_path(model_name, num_of_params, quantization)
    # Check whether the model exists.
    if not os.path.isfile(local_model_path):
        # Download the model.
        model.download(model_name, num_of_params, quantization)
    llama_cpp.run_server(port, local_model_path,
                         force_cpu_only=force_cpu_only,
                         fource_gpu_type=fource_gpu_type)
