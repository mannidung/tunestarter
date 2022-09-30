from distutils.log import debug
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import db
import os
import utils

def read_setup():
    global settings
    settings = utils.read_yaml('./config.yaml')
    if not os.path.exists(settings["storage"]):
        utils.debug_print("Storage folder does not exist, creating...")
        os.mkdir(settings["storage"])
    settings["keeptmp"] = False
    db.setup_db(settings["db"], True)
    utils.debug_print("Setup is : {}".format(settings))