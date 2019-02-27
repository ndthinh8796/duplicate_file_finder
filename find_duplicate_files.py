#!/usr/bin/env python3

import argparse
from os import walk
from os.path import expanduser, join, getsize
from collections import defaultdict
from hashlib import md5


def take_args():
    """ Waypoint1
    Convert argument strings to objects and assign them as attributes of
    the namespace.

    @return: an instance ``argparse.Namespace`` corresponding to the
        populated namespace.
    """
    parser = argparse.ArgumentParser(description='Duplicate Files Finder')
    parser.add_argument('-p', '--path', required=True,
                        help='root directory')
    return parser.parse_args()


def scan_files(path):
    """ Waypoint2
    Takes one argument path corresponding to an absolute path and
    returns a flat list of files scanned recursively from this specified path

    Examples:

        >>> scan_files('~/downloads')
        ['/home/botnet/downloads/heobs/archive.csv',
        '/home/botnet/downloads/heobs/GL0625.jpg',
        ...]


    @return: a file list identified by its absolute path name.
    """
    all_files = []
    for root, dirs, files in walk(path):
        for file in files:
            all_files.append(join(root, file))
    return all_files


def group_files_by_size(file_path_names):
    """ Waypoint3
    Returns a list of groups of at least two files
    that have the same size and ignore empty files

    Example:

        >>> file_path_names = ['/home/botnet/downloads/heobs/archive.csv',
                               '/home/botnet/downloads/heobs/GL0625.jpg',
                               ...]
        >>> group_files_by_size(file_path_names)
        [['/home/botnet/downloads/heobs/GL0701.jpg',
        '/home/botnet/downloads/heritagego/GL0701.jpg'],
        [...]]


    @param file_path_names: list of absolute path files

    @return: list of groups of same size files
    """
    grouped_files = defaultdict(list)
    for file in file_path_names:
        file_size = getsize(file)
        if file_size != 0:
            grouped_files[file_size].append(file)
    return [f_list for f_list in grouped_files.values() if len(f_list) > 1]


def get_file_checksum(file_path):
    """ Waypoint4
    Generate a Hash Value for a file using MD5

    Example:

        >>> get_file_checksum('/home/botnet/downloads/heobs/GL0625.jpg'):
        dd23819ce306f0f1476522c9ce3e0a07'


    @param file_path: a file path name

    @return: hash value of a file as string
    """
    md5 = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(block_size), b''):
             md5.update(chunk)
    return md5.hexdigest()


def group_files_by_checksum (file_path_names):
    grouped_files_by_hash = defaultdict(list)
    for file in file_path_names:
        for file in group:
            grouped_files_by_hash[get_file_checksum(file)].append(file)
    return [f_list for f_list in grouped_files.values() if len(f_list) > 1]


def find_duplicate_files(file_path_names):
    grouped_files_by_size = group_files_by_size(file_path_names)
    return group_files_by_checksum(grouped_files_by_size)


if __name__ == '__main__':
    args = take_args()
    files = scan_files(args.path)
    find_duplicate_files(files)
