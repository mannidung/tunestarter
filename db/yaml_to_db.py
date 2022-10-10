import utils
from .db import *
from .tune import *

def import_yaml(filepath):
        collection = utils.read_yaml(filepath)
        ts_name = collection["name"]
        tunestarter_id = add_tunestarter(ts_name)
        utils.debug_print("Tunestarter \"{}\" created with id {}".format(ts_name, tunestarter_id))
        for set_yaml in collection["sets"]:
            utils.debug_print("Processing set {}".format(set_yaml))
            set_name = ""
            if "name" in set_yaml:
                set_name = set_yaml["name"]
                utils.debug_print("Set with name \"{}\" found".format(set_name))
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
                tune_id = add_tune(set_id, tune_yaml)
                link_set_and_tune(set_id, tune_id, order)
                order = order + 1

def add_tunestarter(name):
    tunestarter_table = get_metadata().tables['tunestarters']
    ins = tunestarter_table.insert().values(name = name)
    try:
        result = get_connection().execute(ins)
        return result.inserted_primary_key[0]
    except:
        tunestarter = tunestarter_table.select().where(tunestarter_table.c.name == name)
        result = get_connection().execute(tunestarter)
        for row in result:
            return row[0]

def add_set(tunestarter_id, name):
    set_table = get_metadata().tables['sets']
    set_id = 0
    try:
        ins = set_table.insert().values(name = name, tunestarter_id = tunestarter_id)
        result = get_connection().execute(ins)
        set_id = result.inserted_primary_key[0]
    except:
        utils.debug_print("set with set name {} and tunestarter id {} already exists".format(name, tunestarter_id))
        set = set_table.select().where(set_table.c.name == name)
        result = get_connection().execute(set)
        for row in result:
            set_id = row[0]
    return set_id

def add_tune(set_id, tune_yaml):
    # If not ID nor name defined, we're doomed. Exit in error
    if ("id" not in tune_yaml) and ("name" not in tune_yaml):
        raise ValueError('Either name or id must be defined')
    if "source" not in tune_yaml:
        raise ValueError('Source needs to be defined')
    tune = {}
    if "id" in tune_yaml:
        tune["source_id"] = tune_yaml["id"]
    else:
        tune["source_id"] = -1
    if "name" in tune_yaml:
        tune["name"] = tune_yaml["name"]
    else:
        tune["name"] = "N/A"
    if "setting" in tune_yaml: 
        tune["source_setting"] = tune_yaml["setting"]
    else:
        tune["source_setting"] = 1
    
    # Get ID of source
    sources_table = get_metadata().tables['sources']
    source = sources_table.select().where(sources_table.c.name == tune_yaml["source"])
    result = get_connection().execute(source)
    source_id = result.fetchone().id
    utils.debug_print("Source ID is {}".format(source_id))
    tune["source"] = source_id

    # Check if tune with name already exists and has been downloaded
    with Session(get_engine()) as session:
        found_tune = session.scalars(select(Tune).where(Tune.name == tune["name"])).first()
        if found_tune != None and found_tune.downloaded_timestamp != None:
            tune["source_id"] = found_tune.source_id

    # Write tune to database
    tunes_table = get_metadata().tables['tunes']
    tune_id = 0
    try:
        ins = tunes_table.insert().values(name = tune["name"],
                                            source = tune["source"],
                                            source_id = tune["source_id"],
                                            source_setting = tune["source_setting"]
                                        )
        result = get_connection().execute(ins)
        tune_id = result.inserted_primary_key[0]
    except:
        utils.debug_print("Tune configuration already exists")
        existing_tune = tunes_table.select().where(tunes_table.c.name == tune["name"],
                                        tunes_table.c.source == tune["source"],
                                        tunes_table.c.source_id == tune["source_id"], 
                                        tunes_table.c.source_setting == tune["source_setting"])
        result = get_connection().execute(existing_tune)
        tune_id = result.fetchone().id

    # Write set and tune to bridging table
    tunes_to_sets_table = get_metadata().tables['tunes_to_sets']
    ins = tunes_to_sets_table.insert().values(tune = tune_id, set = set_id)
    try:
        result = get_connection().execute(ins)
    except:
        utils.debug_print("tunes to set with tune id {} and set id {} already exists".format(tune_id, set_id))
    utils.debug_print("Tune with tuple {}, {}, {} handled successfully".format(tune["name"], tune["source_id"], tune["source_setting"]))
    return tune_id

def link_set_and_tune(set_id, tune_id, order):
    table = get_metadata().tables['tunes_to_sets']
    ins = table.insert().values(set = set_id, tune = tune_id, order = order)
    try:    
        result = get_connection().execute(ins)
        result.inserted_primary_key[0]
        utils.debug_print("Set with id {} and tune with id {} linked, order {}".format(set_id, tune_id, order))
        return
    except:
        utils.debug_print("Linking with set id {}, tune id {}, and order {} already exists, doing nothing...".format(set_id, tune_id, order))
        return

__all__ = ['import_yaml']