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
parser.add_argument('user',
                    metavar='user',
                    type=str,
                    nargs=1,
                    help='thesession.org user name to fetch sets from')
parser.add_argument('--keeptmp',
                    action="store_true",
                    help='the tmp file will be kept after generation is done (good for debugging)')

if __name__ == "__main__":
    #try:
    settings.read_setup()
    args = parser.parse_args()
    
    # Should the temporary directory be kept afterwards?
    if args.keeptmp:
        settings.settings["keeptmp"] = True

    #logger.info("Importing tunestarter from file {}".format(args.filepath[0]))
    #tunestarter_id = yaml_import.import_yaml(args.filepath[0])
    tunestarter_id = yaml_import.thesession_import("intmurr")
    #exit()

    #logger.info("Creating tunestarter PDF")
    #tunestarter = Tunestarter_latex(tunestarter_id)

    #except Exception as e:
    #    logger.error("Exception! Panicking!")
    #    logger.error("{}".format(str(e)))
    #    if os.path.exists(settings.settings["tmp_dir"]):
    #        shutil.rmtree(settings.settings["tmp_dir"])