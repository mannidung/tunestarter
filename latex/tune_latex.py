import logging
import os

import settings
from tunestarter import Tunestarter

logger = logging.getLogger(__name__)
directory_tracker = {}

class Tune_latex:
    def __init__(self, tune):
        logger.debug("Creating Set_latex for set with ID {}".format(tune.id))
        self.tune = tune
        print(self.tune)
        folder_path = Tune_latex.get_set_directory_path(self.tune.rhythm)
        self.filename = "{}.tex".format(self.tune.label)
        self.path = os.path.join(folder_path, self.filename)
        logger.debug("Saving tune latex to path {}".format(self.path))
        self.create_latex()
    
    def create_latex(self):
        logger.debug("Creating latex for tune {}".format(self.tune.name))
        strings = self.get_tune_latex_strings()
        with open(self.path,'w+') as set_file:
            for string in strings:
                set_file.write(string)
        self.write_to_tune_index()
        return
    
    def write_to_tune_index(self):
        logger.debug("Writing file {} to index.".format(self.path))
        with open(os.path.join(directory_tracker[self.tune.rhythm], "00-Index.tex"), 'a') as index_file:
            path = os.path.join("tunes", self.tune.rhythm.replace(" ", "_"), self.filename)
            logger.debug("Writing path {} to tune index.".format(path))
            index_file.write("\n\\input{{./{}}}".format(path))
        return
    
    def get_tune_latex_strings(self):
        strings = []
        strings.append("\\subsection{{ {} }} \n".format(self.tune.title))
        strings.append("\\label{{{}}} \n".format(self.tune.label))
        # First, create shortened ABC
        abc = self.tune.abc

        # Then, write stuff to the latex file

        strings.append("{} \\\\ \n".format(self.tune.title))
        strings.append("Full tune on page ~\pageref{{{}}}\n".format(self.tune.label))
        strings.append("\\begin{{abc}}[name={}] \n".format(self.tune.label))
        strings.append("X: " + "1" + "\n") # THIS ROW IS IMPORTANT! WITHOUT X, PS FILES WILL NOT BE GENERATED!
        strings.append("Z: " + self.tune.transcription + "\n")
        strings.append("M: " + self.tune.metre + "\n")
        strings.append("L: " + self.tune.note_length + "\n")
        strings.append("K: " + self.tune.key + "\n")
        strings.append("R: " + self.tune.rhythm + "\n")
        strings.append(abc + "\n")
        strings.append("\\end{abc}\n")
        return strings


    @classmethod
    def get_set_directory_path(Tune_latex, rhythm):
        logger.debug("Checking if directory path and latex entry exists for rhythm {}".format(rhythm))
        if rhythm in directory_tracker:
            logger.debug("Directory and latex entry for rhythm {} already exists".format(rhythm))
            folder_path = directory_tracker[rhythm]
        else: 
            logger.debug("Directory and latex entry for rhythm {} does not exist".format(rhythm))
            folder_path = os.path.join(settings.settings["tmp_dir"],
                                    "tunes",
                                    rhythm.replace(" ", "_"))
            if not os.path.exists(folder_path):
                logger.debug("Storage folder {} does not exist, creating...".format(folder_path))
                os.mkdir(folder_path)
            index_path = os.path.join(folder_path ,"00-Index.tex")
            with open(index_path, "w") as rhythm_index:
                rhythm_index.write("\section{{{}s}}".format(rhythm.capitalize()))
            with open(os.path.join(settings.settings["tmp_dir"], "Tunes.tex"), 'a') as set_index:
                set_index.write("\\input{{./tunes/{}/00-Index.tex}}\n\\clearpage\n".format(rhythm))
            logger.debug("Setting set directory path for {} to {}".format(rhythm, folder_path))
            directory_tracker[rhythm] = folder_path

        return folder_path