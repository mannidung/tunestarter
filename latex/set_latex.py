import logging
import os

import settings
from tunestarter import Tunestarter

logger = logging.getLogger(__name__)
directory_tracker = {}

class Set_latex:
    def __init__(self, set):
        logger.debug("Creating Set_latex for set with ID {}".format(set.id))
        self.set = set
        folder_path = Set_latex.get_set_directory_path(self.set.rhythm)
        self.filename = "{}.tex".format(self.set.label)
        self.path = os.path.join(folder_path, self.filename)
        logger.debug("Saving set latex to path {}".format(self.path))
        self.tunes = self.set.tunes()
        self.create_latex()

    
    def create_latex(self):
        logger.debug("Creating latex for set {}".format(self.set.name))
        strings = self.get_set_latex_strings()
        with open(self.path,'w+') as set_file:
            for string in strings:
                set_file.write(string)
        self.write_to_set_index()
        return
    
    def write_to_set_index(self):
        logger.debug("Writing file {} to index.".format(self.path))
        with open(os.path.join(directory_tracker[self.set.rhythm], "00-Index.tex"), 'a') as index_file:
            path = os.path.join("sets", self.set.rhythm.replace(" ", "_"), self.filename)
            index_file.write("\n\\input{{./{}}}".format(path))
        return

    def get_set_latex_strings(self):
        strings = []
        strings.append("\\subsection{{ {} }} \n".format(self.set.title))
        strings.append("\\label{{{}}} \n".format(self.set.label))
        for tune in self.tunes:
            # First, create shortened ABC
            abc_split = tune.abc.split('|')
            abc_split = abc_split[:settings.settings["num_measures"]]
            while "" in abc_split: abc_split.remove("") 
            abc_split = [""] + abc_split + [""]
            abc = "|".join(abc_split)
            logger.debug("Modified abc: {}".format(abc))

            # Then, write stuff to the latex file

            strings.append("{} \\\\ \n".format(tune.title))
            strings.append("Full tune on page ~\pageref{{{}}}\n".format(tune.label))
            strings.append("\\begin{{abc}}[name={}-set] \n".format(tune.label))
            strings.append("X: " + "1" + "\n") # THIS ROW IS IMPORTANT! WITHOUT X, PS FILES WILL NOT BE GENERATED!
            strings.append("Z: " + tune.transcription + "\n")
            strings.append("M: " + tune.metre + "\n")
            strings.append("L: " + tune.note_length + "\n")
            strings.append("K: " + tune.key + "\n")
            strings.append("R: " + tune.rhythm + "\n")
            strings.append(abc + "\n")
            strings.append("\\end{abc}\n")
        return strings
    
    @classmethod
    def get_set_directory_path(Set_latex, rhythm):
        logger.debug("Checking if directory path and latex entry exists for rhythm {}".format(rhythm))
        if rhythm in directory_tracker:
            logger.debug("Directory and latex entry for rhythm {} already exists".format(rhythm))
            folder_path = directory_tracker[rhythm]
        else: 
            logger.debug("Directory and latex entry for rhythm {} does not exist".format(rhythm))
            folder_path = os.path.join(settings.settings["tmp_dir"],
                                    "sets",
                                    rhythm.replace(" ", "_"))
            if not os.path.exists(folder_path):
                logger.debug("Storage folder {} does not exist, creating...".format(folder_path))
                os.mkdir(folder_path)
            index_path = os.path.join(folder_path ,"00-Index.tex")
            with open(index_path, "w") as rhythm_index:
                rhythm_index.write("\section{{{} Sets}}".format(rhythm.capitalize()))
            with open(os.path.join(settings.settings["tmp_dir"], "Sets.tex"), 'a') as set_index:
                set_index.write("\\input{{./sets/{}/00-Index.tex}}\n\\clearpage\n".format(rhythm.replace(" ", "_")))
            logger.debug("Setting set directory path for {} to {}".format(rhythm, folder_path))
            directory_tracker[rhythm] = folder_path

        return folder_path
