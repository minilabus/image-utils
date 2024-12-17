#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Remove background of image using pixel value from a position """

import argparse
import os

import imageio.v2 as imageio


def _build_arg_parser():
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument('in_filename',
                   help='Path of the input image.')
    p.add_argument('out_filename',
                   help='Path of the output image.')
    p2 = p.add_mutually_exclusive_group()
    p2.add_argument('--palette', type=int, default=32,
                    help='Number of colors in the palette for GIF (0-64). '
                         '[%(default)s]')
    p.add_argument('--level', type=float, default=10,
                   help='Level of compression (0-100). [%(default)s]')
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

    _, ext = os.path.splitext(args.out_filename)
    if ext in ['.jpg', '.jpeg', '.JPG', '.JPEG']:
        new_img = imageio.imread(args.in_filename)
        new_img = new_img[:, :, 0:3]
        imageio.imwrite(args.out_filename, new_img, quality=args.level)
    elif ext in ['.gif', '.GIF']:
        frames = imageio.mimread(args.in_filename)
        with imageio.get_writer(args.out_filename, mode='I',
                                quantizer=2, palettesize=args.palette) as writer:
            for frame in frames:
                writer.append_data(frame)
    elif ext in ['.mp4', '.MP4', '.avi', '.AVI', '.mov', '.MOV']:
        frames = imageio.mimread(args.in_filename)
        with imageio.get_writer(args.out_filename, mode='I',
                                quality=args.level) as writer:
            for frame in frames:
                writer.append_data(frame)
    else:
        new_img = imageio.imread(args.in_filename)
        imageio.imwrite(args.out_filename, new_img)


if __name__ == "__main__":
    main()
