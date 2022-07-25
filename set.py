import utils
import settings
import os
from tune import Tune

class Set:
    """
    aaa

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
    def __init__(self, tunestarter, name = ""):
        self.tunestarter = tunestarter
        self.name = name
        self.filename = ""
        self.tunes = []
        self.tunetypes = ""
    
    def add_tune(self, tune):
        utils.debug_print("Adds tune ({}, {}, {}) to set {}".format(tune.source, tune.id, tune.setting, self.name))
        self.tunes.append(tune)

    def process_set(self):
        for tune in self.tunes:
            if self.tunetypes == "":
                self.tunetypes = tune.rhythm
            elif self.tunetypes != tune.rhythm:
                self.tunetypes = "mixed"
        if self.name == "":
            for tune in self.tunes:
                self.name = self.name + tune.title + ", "
    
    def create_latex(self):
        file = open(os.path.join(settings.settings["tmpdir"], self.tunetypes, self.name),'w+')