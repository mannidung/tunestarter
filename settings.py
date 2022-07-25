from distutils.log import debug
import os
import utils

def read_setup():
    global settings
    settings = utils.read_yaml('./config.yaml')
    if not os.path.exists(settings["storage"]):
        utils.debug_print("Storage folder does not exist, creating...")
        os.mkdir(settings["storage"])
    utils.debug_print("Setup is : {}".format(settings))