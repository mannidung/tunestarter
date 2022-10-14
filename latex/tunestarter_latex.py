import os
import shutil
import subprocess
import settings
import logging

from .set_latex import Set_latex

from tunestarter import Tunestarter


logger = logging.getLogger(__name__)

pdflatex_command = ["pdflatex",
                        "-synctex=1",
                        "-interaction=nonstopmode",
                        "-file-line-error",
                        "-recorder",
                        "-shell-escape",
                        "Tunestarter.tex"]

class Tunestarter_latex:
    def __init__(self, tunestarter_id):
        logger.debug("Creating Tunestarter_latex for tunestarter with ID {}".format(tunestarter_id))
        self.tunestarter = Tunestarter.get_tunestarter(tunestarter_id)
        self.tunestarter.prepare()
        self.create_tunestarter()

    def create_tunestarter(self):
        logger.debug("Creating tunestarter for tunestarter {}".format(self.tunestarter.name))
        self.prepare_boilerplate()
        self.generate_latex()
        self.generate_pdf()
        #if not settings.settings["keeptmp"]:
        #    cleanup_boilerplate()

    def prepare_boilerplate(self):
        logger.debug("Copying boilerplate to {}".format(settings.settings["tmp_dir"]))
        destination = shutil.copytree("./boilerplate", settings.settings["tmp_dir"])

    def cleanup_boilerplate(self):
        logger.debug("Cleaning up boilerplate, removing directory {}".format(settings.settings["tmp_dir"]))
        shutil.rmtree(settings.settings["tmp_dir"])

    def generate_pdf(self):
        logger.debug("Starting first round of pdflatex, writing output to {}".format(settings.settings["pdflatex_output"]))
        with open(settings.settings["pdflatex_output"], "w") as outfile:
            p = subprocess.Popen(pdflatex_command, cwd=settings.settings["tmp_dir"], stdout=outfile)
            p.wait()

        logger.debug("Starting second round of pdflatex, writing output to {}".format(settings.settings["pdflatex_output"]))
        with open(settings.settings["pdflatex_output"], "a") as outfile:
            q = subprocess.Popen(pdflatex_command, cwd=settings.settings["tmp_dir"], stdout=outfile)
            q.wait()
        logger.debug("Moving generated PDF from {} to ./".format(settings.settings["tmp_dir"]))
        shutil.move(os.path.join(settings.settings["tmp_dir"], "Tunestarter.pdf"), "{}.pdf".format("test"))

    def generate_latex(self):
        logger.debug("Creating latex files for tunestarter {}".format(self.tunestarter.name))
        sets = self.tunestarter.get_sets(order_by="rhythm")
        for set in sets:
            Set_latex(set)
        return None
"""
def create_latex():
        strings = self.get_set_latex_strings()
        file = open(os.path.join(settings.settings["tmp_dir"], self.filename),'w+')
        for string in strings:
            file.write(string)
        file.close()
        self.write_to_latex_index()
    
def write_to_latex_index():
    print(os.path.join(settings.settings["tmp_dir"], "sets",self.tunetypes ,"00-Index.tex"))
    file = open(os.path.join(settings.settings["tmp_dir"], "sets", self.tunetypes ,"00-Index.tex"),'a')
    file.write("\n\\input{{./{}}}".format(self.filename))
    file.close()

def get_set_latex_strings():
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
"""