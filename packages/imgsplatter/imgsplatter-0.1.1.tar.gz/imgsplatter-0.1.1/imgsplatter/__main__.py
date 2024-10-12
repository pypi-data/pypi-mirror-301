#!/usr/bin/env python

"""
Splatter: Create a splatter image by randomly placing and rotating images.

Usage:
    python -m splatter -w 1920 -h 1080 -i image1.png -i image2.png --iterations 500 --min-scale 0.15 --max-scale 0.3 -o output-image.jpg --jpeg-quality 95
"""

from imgsplatter import parse_arguments, splatter


if __name__ == '__main__':
    args = parse_arguments()
    splatter(args)