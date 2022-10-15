import shutil
import db
import os
import utils
import logging

logger = logging.getLogger(__name__)

def read_setup():
    global settings
    
    settings = utils.read_yaml('./config.yaml')
    logging.basicConfig(level=logging.INFO)
    if "debug_mode" in settings:
        if settings["debug_mode"] == True:
            logging.basicConfig(level=logging.DEBUG)
        
    # Clean up any tmp dir that might already exist
    if os.path.exists(settings["tmp_dir"]):
        shutil.rmtree(settings["tmp_dir"])

    settings["keeptmp"] = False
    db.setup_db(settings["db"], True)
    #logger.debug("Setup is : {}".format(settings))