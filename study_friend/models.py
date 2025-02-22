import re
import torch
from .utils import (
    get_parent_model_path,
    get_device,
    Engine
)
from .engine.transformers import (
    load_model_transformers,
    query_transformers
)
from .engine.mlx_vlm import (
    load_model_mlx,
    query_mlx
)

def load_model(engine, model_path, verbose=False):
    """
    This function loads a device-specific AI models from the specified path and returns it along with its associated configuration.
    Args:   model_path (str): The path to the directory where the model files are stored.
            verbose (bool, optional): If set to True, additional information will be printed during the loading process. Default is False.
    Returns:    model (object): The loaded AI model.
                processor (object): The tokenizer or processing function used by the model.
                config (object): Configuration settings for the model.
    """
    if verbose:
        print(f"Loading {model_path} using {engine} engine")
    # retrieve device
    device = get_device()
    # Load the model - based on selected engine
    match engine:
        case Engine.Transformers:
           parent_path = get_parent_model_path(model_path)
           if verbose:
               print(f"Parent model path of {model_path} is: {parent_path}")
           return load_model_transformers(model_path, parent_path, device, verbose)
        case Engine.MLX_VLM:
            return load_model_mlx(model_path, verbose)

def query(engine, model, processor, config, prompt, images, temperature = 0.1, max_tokens = 999, verbose = False):
    """
        This function queries a device-specific model with a prompt and images.
        Args:
            model (str): The model to query with.
            processor (Processor): The processor to use for the model.
            config (Config): The config
        Returns: 
            output (str): The generated text
    """
    # retrieve device
    device = get_device()
    # Query Model - based on selected engine
    match engine:
        case Engine.Transformers:
           return query_transformers(model, processor, config, prompt, images, temperature, max_tokens, device, verbose)
        case Engine.MLX_VLM:
            return query_mlx(model, processor, config, prompt, images, temperature, max_tokens, verbose)

