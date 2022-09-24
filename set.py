import utils
import settings
import os
import hashlib
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
        self.label = hashlib.md5(self.name.encode('utf-8')).hexdigest()
    
    def __str__(self):
        tuneString = ""
        for tune in self.tunes:
            tuneString = tuneString + tune.__str__()
        return "#####\nName: {} \nFilename: {}\nTunetypes: {}\nTunes:{} \n#####".format(self.name,
                                                                        self.filename,
                                                                        self.tunetypes,
                                                                        tuneString)
    
    def add_tune(self, tune):
        utils.debug_print("Adds tune ({}, {}, {}) to set {}".format(tune.source, tune.id, tune.setting, self.name))
        tune.add_set_label(self.label)
        print(self.label)
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
        self.filename = os.path.join("sets", self.tunetypes, "{}.tex".format(self.label))
        self.create_latex()
    
    def create_latex(self):
        strings = self.get_set_latex_strings()
        file = open(os.path.join(settings.settings["tmp_dir"], self.filename),'w+')
        for string in strings:
            file.write(string)
        file.close()
        self.write_to_latex_index()
    
    def write_to_latex_index(self):
        print(os.path.join(settings.settings["tmp_dir"], "sets",self.tunetypes ,"00-Index.tex"))
        file = open(os.path.join(settings.settings["tmp_dir"], "sets", self.tunetypes ,"00-Index.tex"),'a')
        file.write("\n\\input{{./{}}}".format(self.filename))
        file.close()
    
    def get_set_latex_strings(self):
        strings = []
        strings.append("\\subsection{{ {} }} \n".format(self.name))
        strings.append("\\label{{{}}} \n".format(self.label))
        for tune in self.tunes:
            strings.append("{} \\\\ \n".format(tune.title))
            strings.append("Full tune on page ~\pageref{{{}}}\n".format(tune.label))
            strings.append("\\begin{{abc}}[name={}] \n".format(hashlib.md5(tune.title.encode('utf-8')).hexdigest()))
            print(tune.path)
            file = open(tune.path,'r')
            cont = True
            while cont:
                line = file.readline()
                # Skip title, it is already set in the subsection entry above
                if "T:" not in line:
                    strings.append(line)
                # Just include first line of abc notation
                if "|" in line:
                    cont = False
                # If line is empty, then stop the loop
                if not line:
                    break
            strings.append("\\end{abc}\n")
            file.close()
        return strings