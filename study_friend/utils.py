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
    parser.add_argument("-d", "--dir", type=str, default=".", help="The directory from where pdfs are stored.")
    parser.add_argument("-im", "--image_size", type=int, default=DEFAULT_IMAGE_SIZE, help="The size of the images to resize to.")

def add_argument_query(parser):
    """
        This functions adds query arguments to the parser.
    """
    add_argument_convert(parser)
    parser.add_argument("-o", "--output_file", type=str, default=OUTPUT_FILE, help="The file to write the model response into.")
    parser.add_argument("-m", "--model", type=str, default=DEFAULT_MODEL, help="The model to query with.")
    parser.add_argument("-e", "--engine", type=str, default=DEFAULT_ENGINE, choices=[e.value for e in Engine], help=f"Type of Engine to use, can be: {' | '.join([e.value for e in Engine])}")
    parser.add_argument("-tp", "--title_prompt", type=str, default=DEFAULT_TITLE_PROMPT, help="Prompt to use to generate the title of a slidepack.")
    parser.add_argument("-qp", "--question_prompt", type=str, default=DEFAULT_QUESTION_PROMPT, help="Prompt to use to generate questions.")
    parser.add_argument("-aq", "--answer_prompt", type=str, default=DEFAULT_ANSWER_PROMPT, help="Prompt to use to generate answers.")
    parser.add_argument("-g", "--group_size", type=int, default=DEFAULT_GROUP_SIZE, help="The size of the window to group images.")
    parser.add_argument("-t", "--temperature", type=float, default=DEFAULT_TEMPERATURE, help="The temperature to use for sampling.")
    parser.add_argument("-mt", "--max_tokens", type=int, default=DEFAULT_MAX_TOKENS, help="The maximum number of tokens to generate.")
    parser.add_argument("-p", "--prompt", type=str, default=".", help="The prompt to query the model on the provided docs.")
    parser.add_argument("-i", "--images", nargs='+', type=str, default=[], help="Query the following images")

def post_process_arguments(args):
    """
        This function post processes the arguments.
    """
    # check grou_size argument
    if args.group_size == 1:
        # replace pluralities with singularities in question_prompt - for better generation
        for plural, singular in zip(DEFAULT_PLURALITY_INJECTORS, DEFAULT_SINGULARITY_INJECTORS):
            args.question_prompt = re.sub(plural, singular, args.question_prompt)

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