import yaml
import settings

def read_yaml(path):
    with open(path, 'r') as file:
        collection = yaml.safe_load(file)
        return collection