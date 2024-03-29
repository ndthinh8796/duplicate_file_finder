#!/usr/bin/env python3
import argparse
from os import walk, access, R_OK
from os.path import expanduser, join, getsize, isfile, isdir, islink
from io import DEFAULT_BUFFER_SIZE
from collections import defaultdict
from hashlib import md5
from json import dumps


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
    parser.add_argument('-b', '--bonus', action='store_true')
    parser.add_argument('-hr', '--human-readable', action='store_true',
                        help='pretty print')
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
    validate_path(path)
    for root, dirs, files in walk(path):
        for file in files:
            file_path = join(root, file)
            if validate_file(file_path):
                all_files.append(file_path)
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
        'dd23819ce306f0f1476522c9ce3e0a07'


    @param file_path: a file path name

    @return: hash value of a file as string
    """
    file_hash = md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(DEFAULT_BUFFER_SIZE), b''):
            file_hash.update(chunk)
    return file_hash.hexdigest()


def group_files_by_checksum(file_path_names):
    """ Waypoint5
    Group file with the same checksum into a list

    Example:

        >>> file_path_names = ['/home/botnet/downloads/heobs/archive.csv',
                               '/home/botnet/downloads/heobs/GL0625.jpg',
                               ...]
        >>> group_files_by_checksum(file_path_names)
        [['/home/botnet/downloads/heobs/GL0701.jpg',
        '/home/botnet/downloads/heritagego/GL0701.jpg'],
        [...]]


    @param file_path_names: a list of file of the same size

    @return: list of list of file of the same checksum
    """
    grouped_files_by_hash = defaultdict(list)
    for file in file_path_names:
        grouped_files_by_hash[get_file_checksum(file)].append(file)
    return [f_list for f_list in grouped_files_by_hash.values()
            if len(f_list) > 1]


def find_duplicate_files(file_path_names):
    """ Waypoint6
    Returns a list of groups of duplicate files

    Example:

        >>> file_path_names = ['/home/botnet/downloads/heobs/archive.csv',
                               '/home/botnet/downloads/heobs/GL0625.jpg',
                               ...]
        >>> find_duplicate_files(file_path_names)
        [['/home/botnet/downloads/heobs/GL0701.jpg',
        '/home/botnet/downloads/heritagego/GL0701.jpg'],
        [...]]


    @param file_path_names: a list of file paths

    @return: list of list of file of the same content
    """
    grouped_files_by_size = group_files_by_size(file_path_names)
    duplicate_files = []
    for file_group in grouped_files_by_size:
        for duplicate_file_group in group_files_by_checksum(file_group):
            duplicate_files.append(duplicate_file_group)
    return duplicate_files


def validate_file(file_path):
    """ Check if path is a file and can be read and not a symlink """
    return (isfile(file_path) and access(file_path, R_OK)
            and not islink(file_path))


def validate_path(path):
    """ Check if input path is directory and can be read """
    if not isdir(path) or not access(path, R_OK):
        raise ValueError('Directory Error')


def pretty_print(func, file_list, human_readable):
    """ Print to terminal that can be read by human or not """
    if human_readable:
            print(dumps(func(file_list), indent=4))
    else:
        print(dumps(func(file_list)))


"""-----------------BONUS--------------------------------"""


def bonus_group_file(file_names):
    """
    Compare two file at a time and put them to the same list if they have
    the same content
    """
    duplicate_files = []
    visited = []
    for i in range(len(file_names) - 1):
        if file_names[i] not in visited:
            tmp = []
            tmp.append(file_names[i])
            for x in range(i + 1, len(file_names)):
                if file_compare(file_names[i], file_names[x]):
                    tmp.append(file_names[x])
            if len(tmp) > 1:
                duplicate_files.append(tmp)
                visited.extend(tmp)
    return duplicate_files


def file_compare(file_name1, file_name2):
    """
    Divide file content by chunk and compare them together
    """
    with open(file_name1, 'rb') as file1, open(file_name2, 'rb') as file2:
        while True:
            file1_chunk = file1.read(DEFAULT_BUFFER_SIZE)
            file2_chunk = file2.read(DEFAULT_BUFFER_SIZE)
            if file1_chunk != file2_chunk:
                return False
            if not file1_chunk:
                return True


def bonus_find_duplicate_files(file_path_names):
    """ Waypoint6
    Returns a list of groups of duplicate files

    Example:

        >>> file_path_names = ['/home/botnet/downloads/heobs/archive.csv',
                               '/home/botnet/downloads/heobs/GL0625.jpg',
                               ...]
        >>> find_duplicate_files(file_path_names)
        [['/home/botnet/downloads/heobs/GL0701.jpg',
        '/home/botnet/downloads/heritagego/GL0701.jpg'],
        [...]]


    @param file_path_names: a list of file paths

    @return: list of list of file of the same content
    """
    grouped_files_by_size = group_files_by_size(file_path_names)
    duplicate_files = []
    for file_group in grouped_files_by_size:
        for duplicate_file_group in bonus_group_file(file_group):
            duplicate_files.append(duplicate_file_group)
    return duplicate_files


"""-------------------MAIN---------------------"""


def main():
    args = take_args()
    files = scan_files(args.path)
    if args.bonus:
        pretty_print(bonus_find_duplicate_files, files, args.human_readable)
    else:
        pretty_print(find_duplicate_files, files, args.human_readable)


if __name__ == '__main__':
    main()
