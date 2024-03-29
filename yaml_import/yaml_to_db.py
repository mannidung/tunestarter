import utils
import db
import logging
from sqlalchemy import select
from sqlalchemy.orm import Session
from tunestarter import Tune

logger = logging.getLogger(__name__)

def import_yaml(filepath):
        collection = utils.read_yaml(filepath)
        ts_name = collection["name"]
        tunestarter_id = add_tunestarter(ts_name)
        logger.debug("Tunestarter \"{}\" created with id {}".format(ts_name, tunestarter_id))
        for set_yaml in collection["sets"]:
            logger.debug("Processing set {}".format(set_yaml))
            set_name = ""
            if "name" in set_yaml:
                set_name = set_yaml["name"]
                logger.debug("Set with name \"{}\" found".format(set_name))
            else: 
                # Temporary name
                set_name = "TMP-"
                for tune_yaml in set_yaml["tunes"]:
                    if "id" in tune_yaml:
                        set_name = set_name + "{}".format(tune_yaml["id"])
                    elif "name" in tune_yaml:
                        set_name = set_name + "{}".format(tune_yaml["name"])
                    if "setting" in tune_yaml:
                        set_name = set_name + "{}".format(tune_yaml["setting"])
            set_id = add_set(tunestarter_id, set_name)
            order = 1
            for tune_yaml in set_yaml["tunes"]:
                logger.debug("Processing tune {}".format(tune_yaml))
                tune_id = add_tune(set_id, tune_yaml)
                link_set_and_tune(set_id, tune_id, order)
                order = order + 1
        return tunestarter_id

def add_tunestarter(name):
    tunestarter_table = db.get_metadata().tables['tunestarters']
    ins = tunestarter_table.insert().values(name = name)
    try:
        result = db.get_connection().execute(ins)
        return result.inserted_primary_key[0]
    except:
        tunestarter = tunestarter_table.select().where(tunestarter_table.c.name == name)
        result = db.get_connection().execute(tunestarter)
        for row in result:
            return row[0]

def add_set(tunestarter_id, name):
    set_table = db.get_metadata().tables['sets']
    set_id = 0
    try:
        ins = set_table.insert().values(name = name, tunestarter_id = tunestarter_id)
        result = db.get_connection().execute(ins)
        set_id = result.inserted_primary_key[0]
    except:
        logger.debug("set with set name {} and tunestarter id {} already exists".format(name, tunestarter_id))
        set = set_table.select().where(set_table.c.name == name)
        result = db.get_connection().execute(set)
        for row in result:
            set_id = row[0]
    return set_id

def add_tune(set_id, tune_yaml):
    logger.debug("Adding tune {} to set with ID {}".format(tune_yaml, set_id))
    # If not ID nor name defined, we're doomed. Exit in error
    if ("id" not in tune_yaml) and ("name" not in tune_yaml):
        logger.error("Neither name nor ID was defined")
        raise ValueError('Either name or id must be defined')
    if "source" not in tune_yaml:
        logger.error("No source defined")
        raise ValueError('Source needs to be defined')
    tune = {}

    logger.debug("Checking if yaml contains source id.")
    if "id" in tune_yaml:
        logger.debug("Key ID with value {} found in tune\'s yaml. Using this value for source_id".format(tune_yaml["id"]))
        tune["source_id"] = tune_yaml["id"]
    else:
        logger.debug("No key ID found in tune\'s yaml. Using ID -1")
        tune["source_id"] = -1
    
    logger.debug("Checking if yaml contains name.")
    if "name" in tune_yaml:
        logger.debug("Key name with value {} found in tune\'s yaml. Using this value for name".format(tune_yaml["name"]))
        tune["name"] = tune_yaml["name"]
    else:
        logger.debug("No key \'name\' found in tune\'s yaml. Using name N/A")
        tune["name"] = "N/A"

    logger.debug("Checking if yaml contains setting.")
    if "setting" in tune_yaml: 
        logger.debug("Key setting with value {} found in tune\'s yaml. Using this value for source_setting".format(tune_yaml["setting"]))
        tune["source_setting"] = tune_yaml["setting"]
    else:
        logger.debug("No key \'setting\' found in tune\'s yaml. Using setting 1")
        tune["source_setting"] = 1
    
    # Get ID of source
    logger.debug("Get the ID of source")
    sources_table = db.get_metadata().tables['sources']
    source = sources_table.select().where(sources_table.c.name == tune_yaml["source"])
    result = db.get_connection().execute(source)
    source_id = result.fetchone().id
    logger.debug("Source ID is {}".format(source_id))
    tune["source"] = source_id

    # Check if tune with name already exists and has been downloaded
    # Only check this if ID is not set!
    if tune["source_id"] == -1:
        with Session(db.get_engine()) as session:
            found_tune = session.scalars(select(Tune).where(Tune.name == tune["name"])).first()
            if found_tune != None and found_tune.downloaded_timestamp != None:
                tune["source_id"] = found_tune.source_id

    # Write tune to database
    tunes_table = db.get_metadata().tables['tunes']
    tune_id = 0
    try:
        ins = tunes_table.insert().values(name = tune["name"],
                                            source = tune["source"],
                                            source_id = tune["source_id"],
                                            source_setting = tune["source_setting"]
                                        )
        result = db.get_connection().execute(ins)
        tune_id = result.inserted_primary_key[0]
    except:
        logger.debug("Tune configuration already exists")
        existing_tune = tunes_table.select().where(tunes_table.c.name == tune["name"],
                                        tunes_table.c.source == tune["source"],
                                        tunes_table.c.source_id == tune["source_id"], 
                                        tunes_table.c.source_setting == tune["source_setting"])
        result = db.get_connection().execute(existing_tune)
        tune_id = result.fetchone().id

    # Write set and tune to bridging table
    tunes_to_sets_table = db.get_metadata().tables['tunes_to_sets']
    ins = tunes_to_sets_table.insert().values(tune = tune_id, set = set_id)
    try:
        result = db.get_connection().execute(ins)
    except:
        logger.debug("tunes to set with tune id {} and set id {} already exists".format(tune_id, set_id))
    logger.debug("Tune with tuple {}, {}, {} handled successfully, saved with ID {}".format(tune["name"], tune["source_id"], tune["source_setting"], tune_id))
    return tune_id

def link_set_and_tune(set_id, tune_id, order):
    table = db.get_metadata().tables['tunes_to_sets']
    ins = table.insert().values(set = set_id, tune = tune_id, order = order)
    try:    
        result = db.get_connection().execute(ins)
        result.inserted_primary_key[0]
        logger.debug("Set with id {} and tune with id {} linked, order {}".format(set_id, tune_id, order))
        return
    except:
        logger.debug("Linking with set id {}, tune id {}, and order {} already exists, doing nothing...".format(set_id, tune_id, order))
        return

__all__ = ['import_yaml']