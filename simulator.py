# -*- coding: utf-8 -*-
from furina import launcher

launcher.run_server(port=8080, engine_name="llama_cpp",
                    model_name="Qwen3", num_of_params="0.6B",)
