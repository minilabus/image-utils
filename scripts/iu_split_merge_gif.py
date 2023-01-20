#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Crop an image to its bounding box. """

import argparse
import os

import imageio.v2 as imageio


def _build_arg_parser():
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument('in_filenames', nargs='+',
                   help='Path of the input image(s).')
    p2 = p.add_mutually_exclusive_group(required=True)
    p2.add_argument('--out_filename',
                    help='Path of the output image.')
    p2.add_argument('--out_dir',
                    help='Path of the output directory.')
    p.add_argument('-f', dest='force_overwrite', action='store_true',
                   help='Overwrite the output files if they exist.')
    return p


def main():
    parser = _build_arg_parser()
    args = parser.parse_args()

    if len(args.in_filenames) > 1:
        if args.out_filename is None:
            raise IOError(
                'Output filename must be specified for merging files.')
        _, ext = os.path.splitext(args.out_filename)
        if ext not in ['.gif', '.GIF', '.mp4', '.MP4']:
            raise IOError('Output filename must be a GIF or MP4.')
        frames = []
        for filename in args.in_filenames:
            _, ext = os.path.splitext(filename)
            if ext not in ['.jpg', '.JPG', '.jpeg', '.JPEG', '.png', '.PNG'] \
                    and args.out_filename is None:
                raise IOError('Output filename must be specified for JPGs and '
                              'PNGs.')
            if not os.path.isfile(filename):
                raise IOError('{} does not exist.'.format(filename))
            if os.path.isfile(args.out_filename) and not args.force_overwrite:
                raise IOError('{} exists, delete it first.'.format(
                    args.out_filename))

            frames.append(imageio.imread(filename))
        imageio.mimwrite(args.out_filename, frames)
    else:
        _, ext = os.path.splitext(args.in_filenames[0])
        if ext in ['.gif', '.GIF', '.mp4', '.MP4'] and args.out_dir is None:
            raise IOError('Output directory must be specified for GIFs and '
                          'MP4s.')
        if not os.path.isfile(args.in_filenames[0]):
            raise IOError('{} does not exist.'.format(args.in_filenames[0]))
        if not os.path.isdir(args.out_dir):
            os.mkdir(args.out_dir)
        elif not args.force_overwrite:
            raise IOError('{} exists, delete it first.'.format(
                args.out_dir))

        gif = imageio.mimread(args.in_filenames[0])
        for i, frame in enumerate(gif):
            imageio.imwrite('{}/frame_{}.png'.format(args.out_dir, i), frame)


if __name__ == "__main__":
    main()
