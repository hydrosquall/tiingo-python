#!/usr/bin/env python

from __future__ import print_function
import glob
import re
import argparse

fixtures_directory = 'tests/fixtures/'

# restclient api header configuration
zero_api_regex = r'(\[Token )0{40}(\])'
real_api_regex = r'(\[Token ).{40}(\])'
zero_token_string = '[Token ' + 40 * '0' + ']'


def has_api_key(file_name):
    """
    Detect whether the file contains an api key in the Token object that is not 40*'0'.
    See issue #86.
    :param file: path-to-file to check
    :return: boolean
    """
    f = open(file_name, 'r')
    text = f.read()
    if re.search(real_api_regex, text) is not None and  \
            re.search(zero_api_regex, text) is None:
        return True
    return False


def remove_api_key(file_name):
    """
    Change the api key in the Token object to 40*'0'.  See issue #86.
    :param file: path-to-file to change
    """
    with open(file_name, 'r') as fp:
        text = fp.read()
    text = re.sub(real_api_regex, zero_token_string, text)
    with open(file_name, 'w') as fp:
        fp.write(text)
    return


def main(path):
    if path[-1] != '/':
        raise ValueError('Final character in path must be /.')
    n_files_changed = 0
    for filename in glob.glob(path+'*.yaml'):
        if has_api_key(filename):
            remove_api_key(filename)
            n_files_changed += 1
    print("Changed {} files.".format(n_files_changed))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path to test fixtures",
                        nargs='?', default=fixtures_directory)
    args = parser.parse_args()
    main(args.path)
