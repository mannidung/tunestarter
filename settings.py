from distutils.log import debug
import shutil
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import db
import os
import utils
import logging

logger = logging.getLogger(__name__)

def read_setup():
    global settings
    logging.basicConfig(level=logging.DEBUG)
    settings = utils.read_yaml('./config.yaml')
    if not os.path.exists(settings["storage"]):
        logger.debug("Storage folder does not exist, creating...")
        os.mkdir(settings["storage"])
    else: # Remove old storage and create new one
        shutil.rmtree(settings.settings["storage"])
        os.mkdir(settings["storage"])

    # Clean up any tmp dir that might already exist
    if os.path.exists(settings["tmp_dir"]):
        shutil.rmtree(settings["tmp_dir"])

    settings["keeptmp"] = False
    db.setup_db(settings["db"], True)
    #logger.debug("Setup is : {}".format(settings))