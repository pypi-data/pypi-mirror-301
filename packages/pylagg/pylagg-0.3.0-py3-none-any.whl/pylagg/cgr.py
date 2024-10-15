from typing import Dict, Tuple
from io import BytesIO, TextIOWrapper
import math
import os

import numpy as np
import PIL.Image as im
from rich.progress import track

import toml


def contains_valid_characters(input_string: str) -> bool:
    """
    Checks if the given input string contains valid base pair characters
    """    
    for char in input_string:
        if char not in {'A', 'T', 'C', 'G'}:
            return False
    
    return True


def parse_count_file_line(line: str, k: int) -> Tuple[str, int]:
    """
    Reads a line from an input counts file with a given kmer length 'k', returns the tuple: (kmer, count)
    """

    line_split = line.split()
    kmer = line_split[0]
    
    if k > 0 and len(kmer) != k:
        raise Exception(f"The k-mer {kmer} does not match the reported length k={k}.")

    if not contains_valid_characters(kmer):
        raise Exception(f"Invalid k-mer character in k-mer {kmer} (valid characters are A, T, C, G)")

    try:
        count = line_split[1]

        if count == '' or count.isspace():
            raise Exception()
    except:
        raise Exception(f"Count not provided for k-mer: '{kmer}'")

    try:
        count = int(count)
    except ValueError:
        raise Exception(f"Count for k-mer {kmer} must be an integer'")

    if count < 1:
        raise Exception("All k-mer counts must be ≥1")
    
    return (kmer, count)


def count_file_to_dictionary(file: TextIOWrapper) -> Dict[str, int]:
    """
    Takes a counts file as input and outputs a dictionary representation used later for image generation
    """

    k_dict = {}

    with file:
        k = 0

        file.seek(0)

        for line in file:
            if line.isspace() or line == '':
                continue

            (kmer, count) = parse_count_file_line(line, k)
            k_dict.update({kmer : count})

            if k == 0:
                k = len(kmer)

    return k_dict


def calculate_pos(kmer: str, size: int, corner_labels: Tuple[str, str, str, str]) -> Tuple[int, int]:
    """
    Returns the pixel position (x, y) of a kmer in a CGR image with a given size
    """

    x, y = 0, 0

    # use bit shifting instead of division to avoid floating point values
    offset = size >> 1

    bot_left, _, top_right, bot_right = corner_labels

    for base in reversed(kmer):
        if base == top_right or base == bot_right:
            x += offset

        if base == bot_left or base == bot_right:
            y += offset

        offset >>= 1

    return (x, y)


def generate_image_arr(k_dict: Dict[str, int], verbose=True, size=None, log10=True, normalized=True) -> np.ndarray:
    """
    Generates a numpy array representing an image covering RGB channels
    """
    
    k = len(next(iter(k_dict)))  # gets the length of the first key in k_dict

    if size is None:
        size = 2 ** k

    r = np.zeros((size, size))
    g = np.zeros((size, size))
    b = np.zeros((size, size))

    for kmer, count in track(k_dict.items(), disable=not verbose, description="Generating image..."):
        if log10:
            count = math.log10(count)

        # weak H-bonds W = {A, T} and strong H-bonds S = {G, C} on the diagonals
        r_pos = calculate_pos(kmer, size, ('A', 'G', 'T', 'C'))
        r[r_pos] = count
        
        # purine R = {A, G} and pyrimidine Y = {C, T} on the diagonals
        g_pos = calculate_pos(kmer, size, ('A', 'T', 'G', 'C'))
        g[g_pos] = count

        # amino group M = {A, C} and keto group K = {G, T} on the diagonals
        b_pos = calculate_pos(kmer, size, ('A', 'T', 'C', 'G'))
        b[b_pos] = count

    rgb = np.dstack((r, g, b))

    if normalized:
        rgb = rgb / np.max(rgb)

    return (rgb * 255).astype(np.uint8)


def count_file_to_image(input_data: TextIOWrapper, verbose=True, **kwargs) -> im.Image:
    """
    Takes a counts file as input and returns the generated image as an image object
    """

    k_dict = count_file_to_dictionary(input_data)
    chaos = generate_image_arr(k_dict, verbose, **kwargs)
    return im.fromarray(chaos)


def count_file_to_image_file(input_data: TextIOWrapper, output_file: str | BytesIO, output_type="png", verbose=True):
    """
    Takes counts file data and creates an image at the provided file path or buffer with the given output file type
    """
    
    img = count_file_to_image(input_data, verbose)
    img.save(output_file, output_type)


def config_count_file_to_image_file(input_data: TextIOWrapper, output_file: str | BytesIO, config:dict, output_type="png", verbose=True):
    """
    Takes counts file data and creates an image at the provided file path or buffer with the given output file type
    """
    
    config_size = config.get('cgr', {}).get('size', None)  
    config_log = config.get('cgr', {}).get('log10', True)
    config_normalized = config.get('cgr', {}).get('normalized', True)
    config_output = config.get('Files', {}).get('output', None)
    if config_output != None:
        config_output = os.path.join(config_output, output_file)
        output_file = config_output
    
    img = count_file_to_image(input_data, verbose,size=config_size,normalized = config_normalized)
    img.save(output_file, output_type)

    