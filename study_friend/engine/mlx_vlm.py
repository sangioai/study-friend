import torch
from ..utils import (
    get_device
)

# safe-check - import MLX libraries only if the device is MLX-compatible
#TODO: let's find a way to do this better
if get_device() == torch.device("mps"):
    
    from mlx_vlm import load, generate
    from mlx_vlm.prompt_utils import apply_chat_template
    from mlx_vlm.utils import load_config

    def load_model_mlx(model_path, verbose=False):
        """
        This function loads an MLX-specific AI models from the specified path and returns it along with its associated configuration.
        Args:   model_path (str): The path to the directory where the model files are stored.
                verbose (bool, optional): If set to True, additional information will be printed during the loading process. Default is False.
        Returns:    model (object): The loaded AI model.
                    processor (object): The tokenizer or processing function used by the model.
                    config (object): Configuration settings for the model.
        """
        if verbose:
            print(f"Loading {model_path}")
        # Load the model
        model, processor = load(model_path)
        config = load_config(model_path)
        return model, processor, config


    def query_mlx(model, processor, config, prompt, images, temperature = 0.1, max_tokens = 999, verbose = False):
        """
            This function queries a MLX-specific model with a prompt and images.
            Args:
                model (str): The model to query with.
                processor (Processor): The processor to use for the model.
                config (Config): The config
            Returns: 
                output (str): The generated text
        """
        # Apply chat template
        formatted_prompt = apply_chat_template(
            processor, config, prompt, num_images=len(images)
        )
        # Generate output
        output = generate(model, processor, formatted_prompt, images, temperature=temperature, max_tokens=max_tokens,verbose=verbose)
        return output
    
else:
    def load_model_mlx(*args): raise NotImplementedError()
    def query_mlx(*args): raise NotImplementedError()