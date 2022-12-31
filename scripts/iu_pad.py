#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Remove background of image using pixel value from a position """

import argparse
import os

import imageio.v2 as imageio

from image_utils.utils.image import pad_image_to_center


def _build_arg_parser():
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument('in_filename',
                   help='Path of the input image.')
    p.add_argument('out_filename',
                   help='Path of the output image.')
    p2 = p.add_mutually_exclusive_group(required=True)
    p2.add_argument('--dimensions', nargs=2, type=int,
                    help='Dimensions of the image in pixel.')
    p2.add_argument('--add_borders', nargs=2, type=int,
                    help='Scale of the image. [1.0]')
    return p


def main():
    parser = _build_arg_parser()
    args = parser.parse_args()

    img = imageio.imread(args.in_filename)

    if args.add_borders is not None:
        args.dimensions = (args.add_borders[0] + img.shape[0],
                           args.add_borders[1] + img.shape[1])
    else:
        if args.dimensions[0] < img.shape[0] or args.dimensions[1] < img.shape[1]:
            raise ValueError("--dimensions must be larger than image dimensions.")

    padded = pad_image_to_center(img, args.dimensions)
    imageio.imwrite(args.out_filename, padded)


if __name__ == "__main__":
    main()
