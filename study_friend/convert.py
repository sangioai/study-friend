import pdf2image
import os
import argparse
import PIL
from tqdm import tqdm

from .utils import (
    add_argument_convert,
    add_argument_common,
)
def save_images(dirName, images, imageNames, image_size, verbose = False):
    """ 
    This function saves images to a directory.
    Args: dirName (str): The name of the directory to save images.
            images (list): A list of images to save.
            imageNames (list): A list of image names.
            resizeFactor (int): The factor to resize images by. 
    """
    # create if dir does not exists
    try:
        os.makedirs(dirName)
    except:
        if verbose:
            print(f"Directory \"{dirName}\" already exists")
    finally:
        # save images in dir
        for i in range(len(images)):
            # create file name
            fname = os.path.join(dirName, f"{imageNames[i]}.jpeg")
            # calculate best resizeFactor
            resizeFactor = max(1., max(images[i].size)/image_size)
            # if images are too large - let's resize
            images[i] = images[i].resize((int(images[i].size[0]//resizeFactor), int(images[i].size[1]//resizeFactor)), PIL.Image.LANCZOS)
            images[i].save(fname)

def convert_pdfs_to_images(dirName, image_size, verbose = False):
    """
    This function converts pdf files to images and saves them to a directory.
    Args: dirName (str): The name of the directory from where to convert pdf files.
    """
    # save output dirs
    output_dirs = []
    # iterate over pdfs
    for _fileName in tqdm(os.listdir(dirName), desc="Pdf2images"):
        # get complete file name
        fileName = os.path.join(dirName, _fileName)
        # skip if not pdf
        if not os.path.isfile(fileName) or not os.path.splitext(fileName)[1] == ".pdf":
            continue
        if verbose:
            print(f"Converting {fileName}")
        # subdir is just filename without filetype
        subDirName = os.path.splitext(fileName)[0]
        output_dirs += [subDirName]
        # convert slides
        images = pdf2image.convert_from_path(fileName)
        # create images names
        imageNames = [str(i) for i in range(len(images))]
        # save images
        save_images(subDirName, images, imageNames, image_size, verbose)
    return output_dirs

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert pdfs to images.")
    add_argument_convert(parser)
    add_argument_common(parser)
    args = parser.parse_args()
    # let's call the functions with the arguments
    convert_pdfs_to_images(args.dir, args.image_size, args.verbose)