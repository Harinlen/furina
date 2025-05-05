# -*- coding: utf-8 -*-
import os
import subprocess
from furina.lib import path, hardware


def run_server(port: int, model_path: str, ctx_size=None, ngl=None, force_cpu_only=None, fource_gpu_type=None):
    # Decide the platform based on the current hardware.
    platform: str = hardware.decide_hardware(force_cpu_only, fource_gpu_type)
    if platform == "nvidia":
        platform = "cuda"
    else:
        raise RuntimeError(f"Unknown platform {platform} for llama.cpp")
    # Construct the path.
    path_llama_cpp: str = os.path.join(path.PATH_ASSERT_ENGINE, "llama.cpp", platform)
    engine_env = os.environ.copy()
    # Construct the arguments:
    args: list[str] = ["-m", model_path]
    if isinstance(ngl, int):
        args += ["-ngl", str(ngl)]
    if isinstance(ctx_size, int):
        args += ["-c", str(ctx_size)]
    # Enable Flash Attention
    args += ["-fa", "-ctk", "q8_0", "-ctv", "q8_0"]
    # Set the IP and port.
    args += ["--host", "127.0.0.1", "--port", str(port)]
    # Launch the server.
    subprocess.run([
        os.path.join(path_llama_cpp, "llama-server.exe"),
        *args,
    ], env=engine_env, shell=True)
