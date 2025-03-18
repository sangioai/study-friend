import re
from .constants import *

def add_argument_common(parser):
    """
        This functions adds common arguments to the parser.
    """
    parser.add_argument("-v", "--verbose", action="store_true", default=False, help="Enable verbose output.")

def add_argument_convert(parser):
    """
        This functions adds conversion arguments to the parser.
    """
    parser.add_argument("-im", "--image_size", type=int, default=DEFAULT_IMAGE_SIZE, help="The size of the images to resize to.")
    parser.add_argument("-d", "--dir", type=str, default=".", help="The directory from where pdfs and images are stored.")

def add_argument_query(parser):
    """
        This functions adds query arguments to the parser.
    """
    parser.add_argument("-o", "--output_file", type=str, default=OUTPUT_FILE, help="The file to write the model response into.")
    parser.add_argument("-m", "--model", type=str, default=DEFAULT_MODEL, help="The model to query with.")
    parser.add_argument("-e", "--engine", type=str, default=DEFAULT_ENGINE, choices=[e.value for e in Engine], help=f"Type of Engine to use, can be: {' | '.join([e.value for e in Engine])}")
    parser.add_argument("-id", "--image_dir", type=str, default="", help="Direct path of dir containing images to process.")
    parser.add_argument("-tp", "--title_prompt", type=str, default=DEFAULT_TITLE_PROMPT, help="Prompt to use to generate the title of a slidepack.")
    parser.add_argument("-qp", "--question_prompt", type=str, default=DEFAULT_QUESTION_PROMPT, help="Prompt to use to generate questions.")
    parser.add_argument("-aq", "--answer_prompt", type=str, default=DEFAULT_ANSWER_PROMPT, help="Prompt to use to generate answers.")
    parser.add_argument("-g", "--group_size", type=int, default=DEFAULT_GROUP_SIZE, help="The size of the window to group images.")
    parser.add_argument("-t", "--temperature", type=float, default=DEFAULT_TEMPERATURE, help="The temperature to use for sampling.")
    parser.add_argument("-mt", "--max_tokens", type=int, default=DEFAULT_MAX_TOKENS, help="The maximum number of tokens to generate.")
    parser.add_argument("-ci", "--counter_injector", type=str, default=DEFAULT_COUNTER_INJECTOR, help="Counter injector to replace image count in question prompt.")
    parser.add_argument("-si", "--singular_injectors", nargs='+', type=str, default=DEFAULT_SINGULARITY_INJECTORS, help="Array of singular injectors to replace pluralities in question prompt.")
    parser.add_argument("-pi", "--plural_injectors", nargs='+', type=str, default=DEFAULT_PLURALITY_INJECTORS, help="Array of plural injectors to be used when replace them in question prompt.")

def add_argument_display(parser):
    """
        This functions adds display arguments to the parser.
    """
    parser.add_argument("-f", "--file", type=str, required=True, help="The markdown file to display.")
    parser.add_argument("-u", "--url", type=str, default=DEFAULT_URL, help="The url to host the displayed markdown into.")
    parser.add_argument("--here", action="store_true", default=False, help="Whether to avoid displaying the markdown on url, useful to display on python notebooks.")

def extract_url(url):
    """
        This function extract the host and the port from an url.
        Args:
            url (str): The url to extract the host and port from.
        Returns:
            host (str): The host of the url.
            port (str): The port of the url.
    """
    # check if url is consistent
    if not re.match(DEFAULT_URL_REGEX, url):
        raise ValueError("Invalid URL")
    # remove https:// or http://
    if len(parts := url.split("://")) > 1:
        url = parts[1]
    # split the url into host and port
    host = url
    port = None
    if ":" in host:
        host, port = host.split(":")
    return host, port

def standardize_math_formulas(text):
    """
        This function standardizes the math formulas in a markdown text.
        Args:
            text (str): The markdown text to standardize the math formulas in.
        Returns:
            text2 (str): The markdown text with standardized math formulas.
    """
    text2 = text
    # find al math expression in text
    for math in re.findall(DEFAULT_MATH_REGEX, text):
        # remove '\n' -> new lines
        math_oneline = re.sub("\n","",math).strip()
        # replace multiple-line math texts with corresponding one-line math
        text2 = text2.replace(math, math_oneline)
    return text2

def prompt_injection(prompt : str, original_injectors : list, modified_injectors : list) -> str:
    """
        This function modifies a prompt injecting strings in place of others.
        Args:
            prompt (str): The prompt to modify.
            original_injectors (list): Array of injectors to search in prompt.
            original_injectors (list): Array of injectors to substitute into.
        Returns:
            prompt (str): The modified prompt.
    """
    _prompt = prompt
    # replace pluralities with singularities in question_prompt - for better generation
    for origin, mod in zip(original_injectors, modified_injectors):
        _prompt = re.sub(origin, mod, _prompt)
    return _prompt

def print_args(args):
    """
        This function prints the arguments.
    """
    # https://stackoverflow.com/questions/34992524/print-command-line-arguments-with-argparse
    for arg in vars(args):
        print (f"{arg} : {getattr(args, arg)}")

def get_device():
    """
        This functions retrive the correct device for this machine.
    """
    device = torch.device('cpu')
    if torch.cuda.is_available():
        device = torch.device('cuda')
    elif torch.backends.mps.is_available():
        device = torch.device("mps")
    return device

def get_string_variants(strings : list, sep : str, variants = [str.lower, str.capitalize, str.upper]) -> str:
    """
        This functions concatenate variants of some strings, separeted by selected sep.
        Example: strings=["monday","tuesday"], sep="|"  -> [monday|tuesday|Monday|Tuesday|MONDAY|TUESDAY]
    """
    # generate variants for each string
    vs = [sep.join([v(s) for s in strings]) for v in variants]
    # join them all
    return sep.join(vs)

def get_parent_model_path(model_path):
    """
        This function returns the parent model path of a given model path.
        Args:
            model_path (str): The path of the model to get the parent path of.
        Returns:
            parent_model (str): The parent model path, if found.
    """
    model_finetunigs = get_string_variants(DEFAULT_MODEL_FINETUNING_NAMES, "|")
    parent_model = re.search(DEFAULT_MODEL_REGEX.format(model_finetunigs=model_finetunigs), model_path)
    try:
        span = parent_model.span()
        return model_path[span[0]:span[1]]
    except:
        print(f"Could not find parent model of {model_path}, parent found: {parent_model}.\n\
              Returning itself as parent")
    else:
        return model_path