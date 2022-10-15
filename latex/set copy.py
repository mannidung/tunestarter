import utils
import settings
import os
import hashlib
from tune import Tune

class SetLatex:
    def __init__(self, set):
        self.set = set #
        
    
    def __str__(self):
        tuneString = ""
        for tune in self.tunes:
            tuneString = tuneString + tune.__str__()
        return "#####\nName: {} \nFilename: {}\nTunetypes: {}\nTunes:{} \n#####".format(self.name,
                                                                        self.filename,
                                                                        self.tunetypes,
                                                                        tuneString)

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