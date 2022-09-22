import settings
import utils
import setprocessor
from tunestarter import Tunestarter
import argparse

this_setup = None
debug = True

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('filepath',
                    metavar='filepath',
                    type=str,
                    nargs=1,
                    help='path to the tune starter yaml file')

if __name__ == "__main__":
    settings.read_setup()
    args = parser.parse_args()
    tunestarter = Tunestarter()
    tunestarter.create_tunestarter(args.filepath[0])