import mlx.core as mx
from mlx_vlm import load, generate
from mlx_vlm.prompt_utils import apply_chat_template
from mlx_vlm.utils import load_config
import argparse
import os
import re
import numpy as np
from natsort import natsorted

from .utils import (
    add_argument_query,
    add_argument_common,
)
import convert

def load_model(model_path, verbose=False):
    """
    This function loads an AI model from the specified path and returns it along with its associated configuration.
    Args:   model_path (str): The path to the directory where the model files are stored.
            verbose (bool, optional): If set to True, additional information will be printed during the loading process. Default is False.
    Returns:    model (object): The loaded AI model.
                processor (object): The tokenizer or processing function used by the model.
                config (dict): Configuration settings for the model.
    """
    if verbose:
        print(f"Loading {model_path}")
    # Load the model
    model, processor = load(model_path)
    config = load_config(model_path)
    return model, processor, config

def query(model, processor, config, prompt, images, temperature = 0.1, max_tokens = 999, verbose = False):
    """
        This function queries a model with a prompt and images.
        Args:
            model (str): The model to query with.
            processor (Processor): The processor to use for the model.
            config (Config): The config
    """
    # Apply chat template
    formatted_prompt = apply_chat_template(
        processor, config, prompt, num_images=len(images)
    )
    # Generate output
    output = generate(model, processor, formatted_prompt, images, temperature=temperature, max_tokens=max_tokens,verbose=False)
    return output

def groupImages(subDirName, group_size=3, verbose=False):
    """ 
    This function groups images in a directory into windows of a specified size.
    Args:   subDirName (str): The name of the directory from where to group images.
            group_size (int): The size of the window to group images.
    Return: list of grouped file paths
    """
    # skip if not file
    if not os.path.isdir(subDirName):
        return []
    if verbose:
        print(f"Grouping images in {subDirName}:")
    # read dir files
    images = os.listdir(subDirName)
    images = natsorted(images)
    # save images number
    image_size = len(images)
    # get indexees windowed by group_size
    windows = np.arange(image_size+group_size-(image_size)%group_size).reshape((-1,group_size))
    # windowing
    grouped_files = []
    for window in windows:
        files = []
        for i in window:
            # safe check for idx to be in range
            if i >= image_size: 
                break
            # append files
            files += [os.path.join(subDirName,images[i])]
        grouped_files += [files]
    return grouped_files

def queryImages(grouped_files, model, processor, config, title_prompt, question_prompt, answer_prompt, output_file, verbose=False):
    """
    This function queries an image processing model to extract titles and questions from grouped images, then generates answers based on these questions.
    Args:   grouped_files (list): A list of lists containing paths to the images in each group.
                             Each inner list represents a group of files that belong together.
            model: The AI model used for generating text from images or text prompts.
            processor: The tokenizer or processing function used by the model.
            config: Configuration settings for the model and its preprocessing steps.
            title_prompt (str): A prompt to generate the title of the slide-pack.
            question_prompt (str): A prompt to generate questions based on the image content.
            answer_prompt (str): A template string that includes a placeholder for the question.
                             It is used to generate answers based on specific questions.
            output_file (str): The path to the file where the generated text will be appended.
            verbose (bool, optional): If set to True, additional information will be printed during processing. Default is False.
    Returns: None
    """
    with open(output_file, "a") as wfile:
        # extract title
        if len(grouped_files) > 0 and len(grouped_files[0]) > 0:
            # query model - retrieve title of slide-pack
            title = query(model, processor, config, title_prompt, [grouped_files[0][0]])
            if verbose:
                print(f"Model title response: {title}")
            # print the files to have a reference
            wfile.write(f"# {title}\n")
        # extract question-answers
        for images in grouped_files:
            # extract image paths
            if verbose:
                print(f"Querying model on: {images}")
            # query model - retrieve question on slides
            output = query(model, processor, config, question_prompt, images)
            # write the files to have a reference
            wfile.write(f"\nFiles: [{', '.join(images)}]"+"\n")
            # loop over the output lines
            for out in output.split("\n"):
                # check if line contains a question
                if (question := re.findall('[\w\d].*\?$', out)) != []:
                    question = question[0]
                    # query model - retrieve answer on question
                    answer = query(model, processor, config, answer_prompt.format(question=question), images)
                    if verbose:
                        print(f"Model question: {question}")
                        print(f"Model answer: {answer}")
                    # write to file
                    wfile.write(question+"\n")
                    wfile.write(answer+"\n")
                # otherwise print the line
                else:
                    wfile.write(out+"\n")

def beautifyMarkdown(temp_file, output_file, verbose = False):
    """
    This function processes a Markdown file to format it according to specific rules and writes the formatted content to another file.
    Args:   temp_file (str): The path to the input Markdown file that needs to be processed.
            output_file (str): The path to the output file where the formatted content will be saved.
            verbose (bool, optional): If set to True, the function will print additional information during processing. Default is False.
    Returns: None
    """
    with open(temp_file,"r") as rfile:
        with open(output_file,"w") as wfile:
            while (line := rfile.readline()) != "" :
                quest = re.findall('[^\d. ].*\?$', line)
                slide = re.search('(### Slide \d)(.*)$', line)
                files = re.findall('Files: \[.*$', line)
                sep = re.findall('---$', line)
                # add ":question:" mark before each question
                if quest != [] and not slide:
                    quest = "\n:question: " + quest[0] + "\n\n"
                    wfile.write(quest)
                # remove Slide number (misleading since always 1/2/... for each group)
                elif slide:
                    slide = "### Slide " + slide.group(2)
                    wfile.write(slide)
                # add "---" before each group (i.e. before each Files:)
                elif files != []:
                    files = "---\n\n" + files[0] + "\n"
                    wfile.write(files)
                # remove unwanted "---"
                elif sep != []:
                    wfile.write("")
                # line is ok - write it back
                else:
                    wfile.write(line)
    # delete temp file
    os.remove(temp_file)
            

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Creates a file containing question and answers about pdfs slides.")
    add_argument_query(parser)
    add_argument_common(parser)
    args = parser.parse_args()
    # let's use a temp file to store raw responses
    temp_file = args.output_file + "_temp"
    # let's call the functions with the arguments
    dirs = convert.convertPDFtoImages(args.dir, args.image_size)
    # let's load the model
    model, processor, config = load_model(args.model, args.verbose)
    # let's group images
    for d in dirs:
        # group files
        grouped_files = groupImages(d, args.group_size, args.verbose)
        # query model
        queryImages(grouped_files, model, processor, config, args.title_prompt, args.question_prompt, args.answer_prompt, temp_file, args.verbose)
    # let's make the file priettier
    beautifyMarkdown(temp_file, args.output_file)