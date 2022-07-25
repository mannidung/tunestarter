import os
import settings
import utils
import urllib.request

"""Processes a set collection"""
def process_sets(sets):
    for set in sets:
        utils.debug_print("Processing set {}".format(set))
        for tune in set["tunes"]:
            download_tune(tune)

"""Downloads a tune and returns the path to the file"""
def download_tune(tune):
    if tune["source"] == "thesession":
        utils.debug_print("Using source thesession.org")
        if "setting" not in tune:
            utils.debug_print("Tune thesession_{} had no setting specified, using setting 1".format(tune["id"]))
            tune["setting"] = 1
        path = os.path.join(settings.this_setup["storage"],
                                'thesession_{}_{}.abc'.format(tune["id"], tune["setting"]))
        if not os.path.exists(path):
            url = create_thesession_url(tune)
            utils.debug_print("File with path {} does not exist, downloading from url {}".format(path, url))
            urllib.request.urlretrieve(url, path)
        else:
            utils.debug_print("File with path {} already exists".format(path))
        return path
    else:
        utils.debug_print("Unsupported source specified")
        print("Unsupported source")

"""Creates an url to download file from thesession.org"""
def create_thesession_url(tune):
    if "setting" not in tune:
        print("No setting in tune, exiting...")
        exit()
    else:
        return 'https://thesession.org/tunes/{}/abc/{}'.format(tune["id"], tune["setting"])