import settings
import os
import utils
import setprocessor
from tunestarter import Tunestarter
import argparse

this_setup = None
debug = True

parser = argparse.ArgumentParser(prog='tunestarter',
                    description='Create a tunestarter for your session')
parser.add_argument('filepath',
                    metavar='filepath',
                    type=str,
                    nargs=1,
                    help='path to the tune starter yaml file')
parser.add_argument('--keeptmp',
                    action="store_true",
                    help='the tmp file will be kept after generation is done (good for debugging)')

if __name__ == "__main__":
    settings.read_setup()
    args = parser.parse_args()
    if args.keeptmp:
        settings.settings["keeptmp"] = True
    if os.path.exists(settings.settings["tmp_dir"]):
        os.rmdir(settings.settings["tmp_dir"])
    tunestarter = Tunestarter()
    tunestarter.create_tunestarter(args.filepath[0])