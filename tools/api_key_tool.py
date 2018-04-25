from __future__ import print_function
import glob
import re
import argparse

tokenString = '[Token '
fixturesDirectory = 'tests/fixtures/'
zeroapiregex = r'(\[Token )0{40}(\])'
anyapiregex = r'(\[Token ).{40}(\])'
zeroapistring = '[Token '+40*'0'+']'

parser = argparse.ArgumentParser()
parser.add_argument("path", help="path to test fixtures",
                    nargs='?', default=fixturesDirectory)
args = parser.parse_args()

def api_key_detector(file):
    '''
    Detect whether the file contains an api key in the Token object that is not 40*'0'.
    See issue #86.
    :param file: path-to-file to check
    :return: boolean
    '''
    f = open(file, 'r')
    text = f.read()
    if re.search(anyapiregex, text) is not None and  \
            re.search(zeroapiregex, text) is None:
        return True
    return False


def api_key_remover(file):
    '''
    Change the api key in the Token object to 40*'0'.  See issue #86.
    :param file: path-to-file to change
    '''
    f = open(file, 'r')
    text = f.read()
    f.close()
    text = re.sub(anyapiregex, zeroapistring, text)
    f = open(file, 'w')
    f.write(text)
    f.close()
    return


def main(path):
    if path[-1] != '/':
        raise ValueError('Final character in path must be /.')
    nFilesChanged = 0
    for file in glob.glob(path+'*.yaml'):
        if api_key_detector(file):
            api_key_remover(file)
            nFilesChanged += 1
    print("Changed {} files.".format(nFilesChanged))

if __name__ == '__main__':
    main(args.path)
