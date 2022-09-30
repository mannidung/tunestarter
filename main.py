import settings
import os
import shutil
import db
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
    
    # Should the temporary directory be kept afterwards?
    if args.keeptmp:
        settings.settings["keeptmp"] = True

    # Clean up any tmp dir that might already exist
    if os.path.exists(settings.settings["tmp_dir"]):
        shutil.rmtree(settings.settings["tmp_dir"])

    db.import_yaml(args.filepath[0])
    #tunestarter = Tunestarter()
    #tunestarter.create_tunestarter(args.filepath[0])