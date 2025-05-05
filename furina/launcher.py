# -*- coding: utf-8 -*-
import importlib
import os
from .lib import model


def run_server(port: int, engine_name: str,
               model_name: str, num_of_params: str = '', quantization: str='',
               force_cpu_only=None, fource_gpu_type=None):
    # Calculate the model paths.
    local_model_path: str = model.get_local_path(model_name, num_of_params, quantization)
    # Check whether the model exists.
    if not os.path.isfile(local_model_path):
        # Download the model.
        model.download(model_name, num_of_params, quantization)
    # Try to import the engine to use.
    try:
        target_engine = importlib.import_module(f"furina.engine.{engine_name}")
    except Exception:
        raise RuntimeError(f"Failed to load engine {engine_name}")
    # Launch the engine server.
    target_engine.run_server(port, local_model_path,
                             force_cpu_only=force_cpu_only,
                             fource_gpu_type=fource_gpu_type)
