import settings
import os
import shutil
import yaml_import
from latex import Tunestarter_latex
import argparse
import logging

logger = logging.getLogger(__name__)

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
    try:
        settings.read_setup()
        args = parser.parse_args()
        
        # Should the temporary directory be kept afterwards?
        if args.keeptmp:
            settings.settings["keeptmp"] = True

        tunestarter_id = yaml_import.import_yaml(args.filepath[0])
        tunestarter = Tunestarter_latex(tunestarter_id)

    except Exception as e:
        logger.debug("Exception! Panicking!")
        logger.debug("{}".format(str(e)))
        if os.path.exists(settings.settings["storage"]):
            shutil.rmtree(settings.settings["storage"])