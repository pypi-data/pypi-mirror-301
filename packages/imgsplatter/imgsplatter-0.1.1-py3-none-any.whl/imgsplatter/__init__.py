import argparse
import time
import random
from PIL import Image
from tqdm import tqdm

from .splatter import splatter

def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description='Create a splatter image by randomly placing and rotating images.')
    parser.add_argument('-w', '--width', type=int, help='Width of the output image.')
    parser.add_argument('-H', '--height', type=int, help='Height of the output image.')
    parser.add_argument('-i', '--input-image', action='append', required=True, help='Input image(s) to use. At least one is required.')
    parser.add_argument('--iterations', type=int, default=750, help='Number of iterations.')
    parser.add_argument('--min-scale', type=float, default=0.15, help='Minimum scale factor.')
    parser.add_argument('--max-scale', type=float, default=0.325, help='Maximum scale factor.')
    parser.add_argument('-o', '--output-image', help='Output image filename.')
    parser.add_argument('--jpeg-quality', type=int, default=95, help='JPEG quality for output image.')
    return parser.parse_args()
