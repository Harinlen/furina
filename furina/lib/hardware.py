# -*- coding: utf-8 -*-
SIMD_INSTRUCTIONS: list[str] = ['avx512', 'avx2', 'avx']

def get_best_simd_of_cpu() -> str:
    try:
        import cpuinfo
        # Extract the CPU information.
        info = cpuinfo.get_cpu_info()
        instruction_sets: set[str] = set(info['flags'])
        for candidate_instruction in SIMD_INSTRUCTIONS:
            if candidate_instruction in instruction_sets:
                return candidate_instruction
        return ''
    except Exception:
        return ''


def get_gpus() -> list[str]:
    # Logic:
    # 1. When we cannot find any GPU, return ''.
    # 2. When we find only one GPU, return a list of string with only one of the following:
    #      nvidia, amd, intel, moore_threads
    # 3. When we find multiple GPU, return a list of string with all the card type.
    import GPUtil
    gpus: list[str] = []
    for gpu in GPUtil.getGPUs():
        gpu_name: str = gpu.name.lower()
        if 'nvidia' in gpu_name:
            gpus.append('nvidia')
    return gpus


def platform() -> dict:
    return {
        "cpu": get_best_simd_of_cpu(),
        "gpu": get_gpus(),
    }


def decide_hardware(force_cpu_only=None, fource_gpu_type=None) -> str:
    # First extract the hardware information.
    current_platform: dict = platform()
    # Check the force enable switches.
    if isinstance(force_cpu_only, bool) and force_cpu_only:
        return current_platform['cpu']
    # Check whether it provide a force GPU type.
    if isinstance(fource_gpu_type, str):
        # Check whether the GPU contains the type.
        if fource_gpu_type in current_platform['gpu']:
            return fource_gpu_type
    # Or else, the system need to decide one platform.
    if len(current_platform['gpu']) > 0:
        # Use the first GPU type we have.
        return current_platform['gpu'][0]
    return current_platform['cpu']