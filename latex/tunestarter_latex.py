import os
import shutil
import subprocess
import settings
import logging

from .set_latex import Set_latex
from .tune_latex import Tune_latex

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
        if not settings.settings["keeptmp"]:
            self.cleanup_boilerplate()

    def prepare_boilerplate(self):
        logger.debug("Copying boilerplate to {}".format(settings.settings["tmp_dir"]))
        destination = shutil.copytree("./boilerplate", settings.settings["tmp_dir"])

    def cleanup_boilerplate(self):
        logger.debug("Cleaning up boilerplate, removing directory {}".format(settings.settings["tmp_dir"]))
        shutil.rmtree(settings.settings["tmp_dir"])

    def generate_pdf(self):
        logger.debug("Starting first round of pdflatex, writing output to {}".format(settings.settings["pdflatex_output"]))
        with open(settings.settings["pdflatex_output"], "w") as outfile:
            p = subprocess.Popen(pdflatex_command, cwd=settings.settings["tmp_dir"], stdout=outfile, stderr=outfile)
            logger.debug("Latex command is {}".format(p.args))
            p.wait()
        logger.debug("Starting second round of pdflatex, writing output to {}".format(settings.settings["pdflatex_output"]))
        with open(settings.settings["pdflatex_output"], "a") as outfile:
            q = subprocess.Popen(pdflatex_command, cwd=settings.settings["tmp_dir"], stdout=outfile, stderr=outfile)
            logger.debug("Latex command is {}".format(q.args))
            q.wait()
        logger.debug("Moving generated PDF from {} to ./".format(settings.settings["tmp_dir"]))
        shutil.move(os.path.join(settings.settings["tmp_dir"], "Tunestarter.pdf"), "{}.pdf".format(self.tunestarter.name.replace(" ", "_")))

    def generate_latex(self):
        logger.debug("Creating latex files for tunestarter {}".format(self.tunestarter.name))
        sets = self.tunestarter.get_sets(order_by="rhythm")
        for set in sets:
            Set_latex(set)
        tunes = self.tunestarter.get_tunes()
        for tune in tunes:
            Tune_latex(tune, self.tunestarter.id)
        return None
