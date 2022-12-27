#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Remove background of image using pixel value from a position """

import argparse
import os

import imageio.v2 as imageio

from image_utils.utils.image import remove_background


def _build_arg_parser():
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument('in_filename',
                   help='Path of the input image.')
    p.add_argument('out_filename',
                   help='Path of the output image.')
    p.add_argument('--mode', choices=['fill', 'value'], default='fill',
                   help='Either replace all close values or use a floodfill.'
                        '[%(default)s]')
    p.add_argument('--position', nargs=2, type=int, default=[0, 0],
                   help='Position at which the white vs black background is '
                        'detected. [%(default)s]')
    p.add_argument('--threshold', type=float, default=10,
                   help='Threshold for background detection in case of noise. '
                        '[%(default)s]')
    return p


def main():
    parser = _build_arg_parser()
    args = parser.parse_args()
    args.position = tuple(args.position)

    img = imageio.imread(args.in_filename)
    new_img = remove_background(img, args.threshold,
                                args.position, args.mode)
    imageio.imwrite(args.out_filename, new_img)


if __name__ == "__main__":
    main()
