import utils
import os
import settings
import urllib.request as request
import sjkabc

class Tune:
    """
    A tune is a reference to a tune. It contains the source, the ID, the setting, and the path to the file where the abc notation is located.

    ...

    Attributes
    ----------
    source : str
        the source for the tune, currently thesession is supported
    id : str
        the thesession.org id of the tune
    setting : str
        the setting (i.e. version) of the tune on thesession
    exists : boolean
        true if file exists on disk. Does not guarantee integrity.
    url : str
        the url to the abc file of the tune
    path : str
        the path of the abc file on local disk. This being set does not guarantee that the file exists on disk.

    Methods
    -------
    __init__(source, id, setting = 1)
        Prints the animals name and what sound it makes
    check_exists()
        Checks if a file exists at the tune's path
    download()
        Downloads the file from the source and puts it in the storage directory
    """
    def __init__(self, source, id, setting = 1):
        self.source = source
        self.id = id
        self.setting = setting
        self.exists = False
        self.url = ""
        self.path = ""
        self.title = ""
        self.rhythm = ""

        if self.source == "thesession":
            self.url = 'https://thesession.org/tunes/{}/abc/{}'.format(self.id, self.setting)
            utils.debug_print("Source is thesession, setting url to {}".format(self.url))
        else:
            self.url = "undefined"
        self.path = os.path.join(settings.settings["storage"],
                                    'thesession_{}_{}.abc'.format(self.id, self.setting))
        
        self.check_exists()
        

    def check_exists(self):
        if os.path.exists(self.path):
            utils.debug_print("File with path {} already exists, setting tune.existing to True".format(self.path))
            self.exists = True
        else:
            utils.debug_print("File with path {} does not exists, setting tune.existing to False".format(self.path))
            self.exists = False

    def download(self):
        self.check_exists()
        if not self.exists:
            utils.debug_print("File with path {} does not exist, downloading from url {}".format(self.path, self.url))
            request.urlretrieve(self.url, self.path)
            utils.debug_print("File at url {} downloaded to path {}.".format(self.path, self.url))
            self.exists = True
    
    def get_metadata(self):
        if not self.check_exists():
            self.download()
        for tune in sjkabc.parse_file(self.path):
            self.title = tune.title
            self.rhythm = tune.rhythm
