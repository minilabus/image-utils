#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Remove background of image using pixel value from a position """

import argparse
import os

import imageio.v2 as imageio

from image_utils.utils.image import auto_crop


def _build_arg_parser():
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument('in_filename',
                   help='Path of the input image.')
    p.add_argument('out_filename',
                   help='Path of the output image.')
    p.add_argument('--borders', type=int, default=0,
                   help='Border around the bounding box. [%(default)s]')
    return p


def main():
    parser = _build_arg_parser()
    args = parser.parse_args()

    img = imageio.imread(args.in_filename)
    cropped = auto_crop(img, args.borders)
    imageio.imwrite(args.out_filename, cropped)


if __name__ == "__main__":
    main()
