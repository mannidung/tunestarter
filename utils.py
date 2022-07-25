import yaml
import settings

def read_yaml(path):
    with open(path, 'r') as file:
        collection = yaml.safe_load(file)
        return collection

def debug_print(string):
    if settings.settings["debug_mode"]:
        print("DEBUG: {}".format(string))