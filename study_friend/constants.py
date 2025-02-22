import torch
from enum import StrEnum

# CONSTANT - ENGINEs
class Engine(StrEnum):
    Transformers = "transformers",
    MLX_VLM = "mlx_vlm"

# CONSTANTS - device
DEVICE_IS_MLX = torch.mps.is_available()
DEVICE_MEMORY_GB = (torch.cuda.torch.mps.recommended_max_memory() if DEVICE_IS_MLX else torch.cuda.memory.mem_get_info()[1]) / (1<<30) # device memory in GB

# CONSTANTS - parser
DEFAULT_IMAGE_SIZE = 500 #? if DEVICE_MEMORY_GB > 4. else 400 # best image size for 3B/7B models
DEFAULT_GROUP_SIZE = 3 if DEVICE_MEMORY_GB > 4. else 1
DEFAULT_VERBOSE = False
DEFAULT_MODEL = "mlx-community/Qwen2.5-VL-7B-Instruct-4bit" if DEVICE_IS_MLX else ("unsloth/Qwen2.5-VL-7B-Instruct-unsloth-bnb-4bit" if DEVICE_MEMORY_GB > 4. else "unsloth/Qwen2.5-VL-3B-Instruct-unsloth-bnb-4bit")
DEFAULT_TITLE_PROMPT = "\nUse the Format: Title - Subtitle\nExample: Impressionism - Paintings\n\nWhat is the title and subtitle (if not present leave it blank) of the slide? Use the format in the example above."
DEFAULT_PLURALITY_INJECTORS = ['''<Slide's number>''', 'for each slide']
DEFAULT_SINGULARITY_INJECTORS = ['1' , '']
DEFAULT_QUESTION_PROMPT = f"\nExample:\n### Slide {DEFAULT_PLURALITY_INJECTORS[0]}: <Slide's title>\n\n\n1. <question 1>?\n2. <question 2>?\n\nWhat is the subject of the slides? Generate me 2 different questions {DEFAULT_PLURALITY_INJECTORS[1]} about the charts and concepts, don't provide any answer. Use the template of the example above {DEFAULT_PLURALITY_INJECTORS[1]}."
DEFAULT_ANSWER_PROMPT = "\nLook at the images and briefly answer the following question:\n{question}"
OUTPUT_FILE = "output.md"
DEFAULT_TEMPERATURE = 0.1
DEFAULT_MAX_TOKENS = 999
DEFAULT_ENGINE = Engine.MLX_VLM if DEVICE_IS_MLX else Engine.Transformers

# CONSTANTS - models
DEFAULT_MODEL_FINETUNING_NAMES = ["base","instruct","coder"]
DEFAULT_MODEL_REGEX = '(.*)/(.*)-(\\d*[B|M])(-)?({model_finetunigs})?'
