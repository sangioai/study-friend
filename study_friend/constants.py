import torch
from enum import StrEnum

# CONSTANT - ENGINEs
class Engine(StrEnum):
    Transformers = "transformers",
    MLX_VLM = "mlx_vlm"

# CONSTANTS - device
DEVICE_IS_MLX = torch.backends.mps.is_available()
DEVICE_MEMORY_GB = (torch.mps.recommended_max_memory() if DEVICE_IS_MLX else torch.cuda.memory.mem_get_info()[1]) / (1<<30) # device memory in GB

# CONSTANTS - query
DEFAULT_IMAGE_SIZE = 500 #? if DEVICE_MEMORY_GB > 4. else 400 # best image size for 3B/7B models
DEFAULT_GROUP_SIZE = 3 if DEVICE_MEMORY_GB > 4. else 1
DEFAULT_VERBOSE = False
DEFAULT_MODEL = "mlx-community/Qwen2.5-VL-7B-Instruct-4bit" if DEVICE_IS_MLX else ("unsloth/Qwen2.5-VL-7B-Instruct-unsloth-bnb-4bit" if DEVICE_MEMORY_GB > 4. else "unsloth/Qwen2.5-VL-3B-Instruct-unsloth-bnb-4bit")
DEFAULT_TITLE_PROMPT = "\nWhat is the slide title and slide subtitle (if not present leave it blank) of the slide? Answer concisely using the following template and nothing else:\n<slide_title> - <slide_subtitle>"
DEFAULT_COUNTER_INJECTOR = "<<number_of_slides>>"
DEFAULT_PLURALITY_INJECTORS = ['''<Slide's number>''', f'for each of the {DEFAULT_COUNTER_INJECTOR} slide']
DEFAULT_SINGULARITY_INJECTORS = ['1' , '']
DEFAULT_QUESTION_PROMPT = f"\nExample:\n### Slide {DEFAULT_PLURALITY_INJECTORS[0]}: <Slide's title>\n\n\n1. <question 1>?\n2. <question 2>?\n\nWhat is the subject of the slides? Generate me 2 different questions {DEFAULT_PLURALITY_INJECTORS[1]} about the charts and concepts, don't provide any answer. Use the template of the example above {DEFAULT_PLURALITY_INJECTORS[1]}."
DEFAULT_ANSWER_PROMPT = "\nLook at the images and briefly answer the following question:\n{question}"
OUTPUT_FILE = "output.md"
DEFAULT_TEMPERATURE = 0.1
DEFAULT_MAX_TOKENS = 999
DEFAULT_ENGINE = Engine.MLX_VLM if DEVICE_IS_MLX else Engine.Transformers
# CONSTANTS - display
DEFAULT_URL = "http://127.0.0.1:5000"
DEFAULT_URL_REGEX = r"^(https?://)?([a-zA-Z0-9.-])+(:[0-9]+)?$"
DEFAULT_HTML_IMAGE = "<img src=\"{file}\" alt=\"{file}\">"
DEFAULT_HTML_DIV = """<div style="display: flex; flex-direction: row; flex-wrap: wrap; ">{images}</div>"""
DEFAULT_HTML_STYLE = """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/default.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js"></script> <script>hljs.highlightAll();</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
<style> html { display: flex;} p { display: block;} p,a,li {font-size: 16px;} body {font-family: -apple-system, BlinkMacSystemFont, &quot;Segoe UI&quot;, &quot;Noto Sans&quot;, Helvetica, Arial, sans-serif, &quot;Apple Color Emoji&quot;, &quot;Segoe UI Emoji&quot;font-size: 16px; display: block; margin: 20px;} .dark-mode {background-color: #0d1116ff;color: rgb(240, 246, 252);} .dark-mode > button > .dark-theme-img {filter: invert(1)} </style>
<script>function toggleDark() {document.body.classList.toggle("dark-mode");}</script>
<button onclick="toggleDark()"  style="position: fixed;right: 20px;top: 20px;background-color: transparent;border: none;"><img class="dark-theme-img" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAhGVYSWZNTQAqAAAACAAFARIAAwAAAAEAAQAAARoABQAAAAEAAABKARsABQAAAAEAAABSASgAAwAAAAEAAgAAh2kABAAAAAEAAABaAAAAAAAAAEgAAAABAAAASAAAAAEAA6ABAAMAAAABAAEAAKACAAQAAAABAAAAFKADAAQAAAABAAAAFAAAAABB553+AAAACXBIWXMAAAsTAAALEwEAmpwYAAABWWlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNi4wLjAiPgogICA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPgogICAgICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgICAgICAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyI+CiAgICAgICAgIDx0aWZmOk9yaWVudGF0aW9uPjE8L3RpZmY6T3JpZW50YXRpb24+CiAgICAgIDwvcmRmOkRlc2NyaXB0aW9uPgogICA8L3JkZjpSREY+CjwveDp4bXBtZXRhPgoZXuEHAAACN0lEQVQ4Ea2VPYsTQRjHM7vJCoEgR3JXhryUObAItgp+Am1UsLwPEEQU9ANoIYiptLM6kGu0tdT2CFhcKskLKeUum8aASXbH33+ZOU8UdY974OGZmWfmv8/7msJPMiwDOOl0OtFyubzN+ia8C9fgLfjEWnsYBMH+eDx+yz6FQyctsiAQkZe22WwK6DmP6lIAIN6wfAXvwDeKxeL2ZrOJubM3Go3ecXb6XovTTavVemmM6TmQNTp9NYKPJ5PJNjKjRqNxnXv9Uql0Zb1ev0D3AEWGI3MzkwXGF3tpmgpIVIQDHuri92q1+iaO42+szWKxmMKvK5XKpSiKHiEvs/+ALsxi1sRNWZYkicBKUsC/ELqVOzDdbld3zHQ6fbJarZ4Ber/dbt/iLDEuAV8ArONqwuFZMCsLOY8BbM9ms1hAsEIhYyQV98/IOq7XAmVTCeCRrDsLxvavlGKpwqKk9UjUFmG7q6+oNM5Fg8FA2S/g+key/pX43xPgLl/QudZ5ybp46t0nonNVIFWH4svHbXOLCS9q57Hqj19S7qQQ4Im7kR24dW5B2Fo8OhbgEegCUF/mJUNifCNcA/RQgO/zovj7vmzUipTNDuW3H5TL5QPSPcNKVb8K+38p8GXD276GhSZQMBwO1VIP/+U2X/cx9q2nvcW6pxoS6PfYp3I5pGUO8L8fhqGsVEx+sxSdpo7IurhlYPTxY00cN8ZCZcPXn72I8eXBvLyQAZv54SxVCBK103w+v8M69y/gB8cmIeMqPC5mAAAAAElFTkSuQmCC" alt="Red dot"></button>
<p style="position: fixed; bottom: 10px; margin: 0; width: 100%; text-align: center; display: block">Made with <a href="https://github.com/sangioai/study-friend/tree/master?tab=readme-ov-file">StudyFriend&#128218</a></p>
"""

# CONSTANTS - models
DEFAULT_MODEL_FINETUNING_NAMES = ["base","instruct","coder"]
DEFAULT_MODEL_REGEX = '(.*)/(.*)-(\\d*[B|M])(-)?({model_finetunigs})?'
