from db import *
import logging
from . import Tune, Set

from sqlalchemy import Column
from sqlalchemy import Integer, String
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger(__name__)

Base = declarative_base()

class Tunestarter(Base):
    __tablename__ = 'tunestarters'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    def __repr__(self):
        return "\n\t---\n\t"\
                "ID: {} \n\t"\
                "Name: {}\n\t"\
                "---\n".format(self.id,
                                self.name
                                )

    def process(self):
        logger.debug("Processing tunestarter {} with ID {}".format(self.name, self.id))
        self.prepare()

    def prepare(self):
        logger.debug("Preparing tunestarter {} with ID {}".format(self.name, self.id))
        # First, download tunes if they aren't already prepared
        logger.debug("Downloading tunes...")
        Tune.download_tunes()
        logger.debug("Downloading sets done")
        logger.debug("Preparing sets...")
        self.prepare_sets()
        logger.debug("Sets of tunestarter {} prepared".format(self.name))

    def prepare_sets(self):
        sets = self.get_sets()
        for set in sets:
            set.prepare_set()

    def get_sets(self):
        with Session(get_engine()) as session:
            sets = session.scalars(select(Set).where(Set.tunestarter_id == self.id)).all()
            return sets
    
    @classmethod
    def get_tunestarter(Tunestarter, id):
        logger.debug("Return tunestarter object for tunestarter with ID {}".format(id))
        with Session(get_engine()) as session:
            tunestarter = session.scalars(select(Tunestarter).where(Tunestarter.id == id)).first()
            return tunestarter