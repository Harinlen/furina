# -*- coding: utf-8 -*-
import os
import requests
from pathlib import PurePosixPath
from . import path


MODEL_CONFIG: dict[str, dict] = {
    "Qwen3": {"user": "unsloth", "q": "BF16"},
    "DeepSeek-R1": {"user": "unsloth", "q": "BF16"},
    "DeepSeek-R1-Distill-Qwen": {"user": "unsloth", "q": "BF16"},
}

def get_local_name(model_name: str, num_of_params: str = '', quantization: str='') -> str:
    # Based on the model name, construct the URL.
    if model_name not in MODEL_CONFIG:
        raise NotImplementedError(f"Unsupported model {model_name}")
    # Extract the model config:
    model_config: dict = MODEL_CONFIG[model_name]
    # Calculate the model paths.
    local_name: str = model_name.lower()
    if len(num_of_params) > 0:
        local_name += f"-{num_of_params.lower()}"
    if len(quantization) == 0:
        quantization = model_config["q"]
    local_name += f"_{quantization.lower()}"
    return f"{local_name}.gguf"


def get_local_path(model_name: str, num_of_params: str = '', quantization: str='') -> str:
    return os.path.join(path.PATH_ASSERT_MODEL, get_local_name(model_name, num_of_params, quantization))


def download(model_name: str, num_of_params: str = '', quantization: str = ''):
    # Based on the model name, construct the URL.
    if model_name not in MODEL_CONFIG:
        raise NotImplementedError(f"Unsupported model {model_name}")
    # Extract the model config:
    model_config: dict = MODEL_CONFIG[model_name]
    # Calculate the repo name and file name.
    model_file_name: str = model_name
    model_repo_name: str = model_name
    if len(num_of_params) > 0:
        model_repo_name += f"-{num_of_params}"
        model_file_name += f"-{num_of_params}"
    if len(quantization) == 0:
        quantization = model_config["q"]
    model_file_name += f"-{quantization}.gguf"
    model_repo_name += "-GGUF"
    # Get the user we want.
    user: str = model_config["user"]
    # Calculate the model file name.
    if not os.path.isdir(path.PATH_ASSERT_MODEL):
        os.makedirs(path.PATH_ASSERT_MODEL, exist_ok=True)
    local_model_path: str = get_local_path(model_name, num_of_params, quantization)
    # Calculate the model url.
    target_url: str = "https://" + str(PurePosixPath("hf-mirror.com").joinpath(user, model_repo_name, "resolve", "main", model_file_name)) + "?download=true"
    # This will automatically follow redirects
    headers: dict = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    # Create a request with headers
    try:
        response = requests.get(target_url, headers=headers, stream=True)
        response.raise_for_status()  # Check for HTTP errors
        with open(local_model_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    except Exception:
        raise
