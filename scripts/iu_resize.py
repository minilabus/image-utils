#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Resize an image to a given size or scale. """

import argparse
import os

import imageio.v2 as imageio

from image_utils.utils.image import resize


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
    p2.add_argument('--scale', type=float,
                    help='Scale of the image. [1.0]')
    p2.add_argument('--ratio_frac', type=float,
                    help='Ratio of the image (X/Y). [1.0]')
    p2.add_argument('--ratio_val', nargs=2, type=float,
                    help='Ratio of the image as X & Y. [1.0 1.0]')
    p.add_argument('-f', dest='force_overwrite', action='store_true',
                   help='Overwrite the output files if they exist.')
    return p


def main():
    parser = _build_arg_parser()
    args = parser.parse_args()

    if not os.path.isfile(args.in_filename):
        raise IOError('{} does not exist.'.format(args.in_filename))

    if os.path.isfile(args.out_filename) and not args.force_overwrite:
        raise IOError('{} exists, delete it first.'.format(args.out_filename))

    img = imageio.imread(args.in_filename)
    resized = resize(img, args.ratio_frac, args.ratio_val, args.dimensions,
                     args.scale)
    imageio.imwrite(args.out_filename, resized)


if __name__ == "__main__":
    main()
