import settings
import utils
import setprocessor
from tunestarter import Tunestarter

this_setup = None
debug = True

if __name__ == "__main__":
    settings.read_setup()
    tunestarter = Tunestarter()
    tunestarter.create_tunestarter("./example.yaml")
    #collection.prepare_boilerplate()
    #collection.cleanup_boilerplate()
    #sets = utils.read_yaml("./example.yaml")
    #setprocessor.process_sets(sets["sets"])