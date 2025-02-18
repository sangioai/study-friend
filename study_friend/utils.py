import argparse

# Constants
DEFAULT_IMAGE_SIZE = 500
DEFAULT_GROUP_SIZE = 3
DEFAULT_VERBOSE = False
DEFAULT_MODEL = "mlx-community/Qwen2.5-VL-7B-Instruct-4bit"
DEFAULT_TITLE_PROMPT = "Format: Slide's title - Slide's subtitle\nExample: Impressionism - Daga paintings\n\nWhat is the title and subtitle (if not present leave it blank) of the slide? Use the format in the example above."
DEFAULT_QUESTION_PROMPT = "Example:\n### Slide <Slide's number>: <Slide's title>\n\n\n1. <question 1>?\n2. <question 2>?\n\nWhat is the subject of the slides? Generate me 2 different questions for each slide about the charts and concepts, don't provide any answer. Use the template of the example above for each slide."
DEFAULT_ANSWER_PROMPT = "Look at the images and briefly answer the following question:\n{question}"
OUTPUT_FILE = "output.md"
DEFAULT_TEMPERATURE = 0.1
DEFAULT_MAX_TOKENS = 999


def add_argument_common(parser):
    parser.add_argument("-v", "--verbose", action="store_true", default=False, help="Enable verbose output.")

def add_argument_convert(parser):
    """
        This functions adds arguments to the parser.
    """
    parser.add_argument("-d", "--dir", type=str, default=".", help="The directory from where pdfs are stored.")
    parser.add_argument("-im", "--image_size", type=int, default=DEFAULT_IMAGE_SIZE, help="The size of the images to resize to.")

def add_argument_query(parser):
    """
        This functions adds arguments to the parser.
    """
    add_argument_convert(parser)
    parser.add_argument("-o", "--output_file", type=str, default=OUTPUT_FILE, help="The file to write the model response into.")
    parser.add_argument("-m", "--model", type=str, default=DEFAULT_MODEL, help="The model to query with.")
    parser.add_argument("-tp", "--title_prompt", type=str, default=DEFAULT_TITLE_PROMPT, help="Prompt to use to generate the title of a slidepack.")
    parser.add_argument("-qp", "--question_prompt", type=str, default=DEFAULT_QUESTION_PROMPT, help="Prompt to use to generate questions.")
    parser.add_argument("-aq", "--answer_prompt", type=str, default=DEFAULT_ANSWER_PROMPT, help="Prompt to use to generate answers.")
    parser.add_argument("-g", "--group_size", type=int, default=DEFAULT_GROUP_SIZE, help="The size of the window to group images.")
    parser.add_argument("-t", "--temperature", type=float, default=DEFAULT_TEMPERATURE, help="The temperature to use for sampling.")
    parser.add_argument("-mt", "--max_tokens", type=int, default=DEFAULT_MAX_TOKENS, help="The maximum number of tokens to generate.")
    parser.add_argument("-p", "--prompt", type=str, default=".", help="The prompt to query the model on the provided docs.")
    parser.add_argument("-i", "--images", nargs='+', type=str, default=[], help="Query the following images")
