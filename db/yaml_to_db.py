import utils
from .db import *

def import_yaml(filepath):
        collection = utils.read_yaml(filepath)
        ts_name = collection["name"]
        tunestarter_id = add_tunestarter(ts_name)
        utils.debug_print("Tunestarter \"{}\" created with id {}".format(ts_name, id))
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
            add_set(tunestarter_id, set_name)
            #set = Set(self, name)
            """
            for tune_yaml in set_yaml["tunes"]:
                tune = Tune(tune_yaml)
                self.add_tune(tune, set)
            self.add_set(set)
            """

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
    ins = set_table.insert().values(name = name)
    set_id = 0
    try:    
        result = get_connection().execute(ins)
        set_id = result.inserted_primary_key[0]
    except:
        set = set_table.select().where(set_table.c.name == name)
        result = get_connection().execute(set)
        for row in result:
            set_id = row[0]

    tunestarters_to_sets_table = get_metadata().tables['tunestarters_to_sets']
    ins = tunestarters_to_sets_table.insert().values(tunestarter = tunestarter_id, set = set_id)
    try:
        result = get_connection().execute(ins)
    except:
        utils.debug_print("tunestarter to set with tunestarter id {} and set id {} already exists".format(tunestarter_id, set_id))
    return set_id

__all__ = ['import_yaml']