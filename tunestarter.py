import os
from signal import pause
import utils
import shutil
import settings
import subprocess
from set import Set
from tune import Tune

class Tunestarter:
    pdflatex_comamnd = ["pdflatex",
                        "-synctex=1",
                        "-interaction=nonstopmode",
                        "-file-line-error",
                        "-recorder",
                        "-shell-escape",
                        "Tunestarter.tex"]

    def __init__(self):
        self.name = ""
        self.sets = []
        self.tunes = []

    def create_tunestarter(self, filepath):
        self.prepare_boilerplate()
        self.process_yaml(filepath)
        self.download_tunes()
        self.prepare_sets_and_tunes()
        p = subprocess.Popen(self.pdflatex_comamnd, cwd=settings.settings["tmp_dir"])
        p.wait()
        q = subprocess.Popen(self.pdflatex_comamnd, cwd=settings.settings["tmp_dir"])
        q.wait()
        shutil.move(os.path.join(settings.settings["tmp_dir"], "Tunestarter.pdf"), "{}.pdf".format(self.name))
        if not settings.settings["keeptmp"]:
            self.cleanup_boilerplate()


    def add_set(self, set):
        utils.debug_print("Adds set {} to collection {}".format(set, self.name))
        self.sets.append(set)
    
    def add_tune(self, tune, set):
        utils.debug_print("Adds tune ({}, {}, {}) to collection {} and set {}".format(tune.source, tune.id, tune.setting, self.name, set))
        self.tunes.append(tune)
        set.add_tune(tune)

    def process_yaml(self, filepath):
        collection = utils.read_yaml(filepath)
        self.name = collection["name"]
        for set_yaml in collection["sets"]:
            utils.debug_print("Processing set {}".format(set_yaml))
            name = ""
            if "name" in set_yaml:
                name = set_yaml["name"]
                print(name)
            set = Set(self, name)
            for tune_yaml in set_yaml["tunes"]:
                tune = Tune(tune_yaml)
                self.add_tune(tune, set)
            self.add_set(set)
    
    def download_tunes(self):
        for tune in self.tunes:
            tune.download()
            tune.get_metadata()
    
    def prepare_sets_and_tunes(self):
        tunes = []
        for set in self.sets:
            set.process_set()
            for tune in set.tunes:
                tunes.append(tune)
            #print(set)
        sorted_tunes = sorted(tunes, key=lambda x: x.title, reverse=False)
        for tune in sorted_tunes:
            tune.create_latex()
            #print(tune)
    
    def prepare_boilerplate(self):
        destination = shutil.copytree("./boilerplate", settings.settings["tmp_dir"]) 
    
    def cleanup_boilerplate(self):
        shutil.rmtree(settings.settings["tmp_dir"])

