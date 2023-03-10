#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Generate a mosaic from a set of images. """

import argparse
import os

import imageio.v2 as imageio
import numpy as np

from image_utils.utils.image import generate_mosaic


def _build_arg_parser():
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument('in_filename', nargs='+',
                   help='Path of the input images.')
    p.add_argument('out_filename',
                   help='Path of the output image.')

    p.add_argument('--rows', type=int, default=None,
                   help='Number of rows in the mosaic. [%(default)s]')
    p.add_argument('--cols', type=int, default=None,
                   help='Number of columns in the mosaic. [%(default)s]')
    p.add_argument('--max_in_row', type=int, default=None,
                   help='Maximum number of images in a row. [%(default)s]')
    p.add_argument('--max_in_col', type=int, default=None,
                   help='Maximum number of images in a column. [%(default)s]')

    p.add_argument('--squarish', action='store_true',
                   help='Try to make the mosaic a square.')
    p.add_argument('--auto_crop', action='store_true',
                   help='Crop the image to the bounding box.')
    p.add_argument('--auto_border', action='store_true',
                   help='Add extra borders.')

    p.add_argument('--scaling_method', choices=['resize_to_avg',
                                                'resize_to_max',
                                                'pad_to_max'],
                   default='resize_to_avg',
                   help='Method to use to scale the images. [%(default)s]')
    p.add_argument('-f', dest='force_overwrite', action='store_true',
                   help='Overwrite the output files if they exist.')
    return p


def main():
    parser = _build_arg_parser()
    args = parser.parse_args()

    for filename in args.in_filename:
        if not os.path.isfile(filename):
            raise IOError('{} does not exist.'.format(filename))

    if os.path.isfile(args.out_filename) and not args.force_overwrite:
        raise IOError('{} exists, delete it first.'.format(args.out_filename))

    if args.rows is not None and args.max_in_col is not None:
        raise ValueError("Cannot specify both --rows and --max_in_col.")

    if args.max_in_row and args.max_in_col:
        raise ValueError("Cannot specify both --max_in_row and --max_in_col.")

    if args.max_in_row:
        args.cols = args.max_in_row
        args.rows = np.ceil(len(args.in_filename) / args.max_in_row)
    elif args.max_in_col:
        args.rows = args.max_in_col
        args.cols = np.ceil(len(args.in_filename) / args.max_in_col)

    if args.rows is None and args.cols is None \
            and args.max_in_row is None and args.max_in_col is None:
        args.rows = 1
        args.cols = len(args.in_filename)

    if args.rows is not None and args.cols is None:
        args.cols = np.ceil(len(args.in_filename) / args.rows)

    if args.cols is not None and args.rows is None:
        args.rows = np.ceil(len(args.in_filename) / args.cols)

    if args.cols * args.rows < len(args.in_filename):
        raise ValueError("Not enough rows and columns to display all images.")

    if args.auto_border and not args.auto_crop:
        raise ValueError("--auto_border requires --auto_crop.")

    if args.squarish:
        print('Overwriting rows and column to make the mosaic squarish.')
        args.rows = args.cols = np.ceil(np.sqrt(len(args.in_filename)))

    imgs = [imageio.imread(f) for f in args.in_filename]
    mosaic = generate_mosaic(imgs, int(args.rows), int(args.cols),
                             args.auto_crop, args.auto_border,
                             args.scaling_method)

    imageio.imwrite(args.out_filename, mosaic)


if __name__ == "__main__":
    main()
