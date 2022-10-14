from unittest import case
import db
import logging
from . import Tune, Set

from sqlalchemy import Column
from sqlalchemy import Integer, String
from sqlalchemy import select
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

    def get_sets(self, order_by="id"):
        with Session(db.get_engine()) as session:
            if order_by == "id":
                logger.debug("Returning sets ordered by id")
                return session.scalars(select(Set)
                                        .where(Set.tunestarter_id == self.id)
                                        .order_by(Set.id)).all()
            elif order_by == "name":
                logger.debug("Returning sets ordered by name")
                return session.scalars(select(Set)
                                        .where(Set.tunestarter_id == self.id)
                                        .order_by(Set.name)).all()
            elif order_by == "title":
                logger.debug("Returning sets ordered by title")
                return session.scalars(select(Set)
                                        .where(Set.tunestarter_id == self.id)
                                        .order_by(Set.title)).all()
            elif order_by == "rhythm":
                logger.debug("Returning sets ordered by rhythm")
                return session.scalars(select(Set)
                                        .where(Set.tunestarter_id == self.id)
                                        .order_by(Set.rhythm)).all()
            else:
                logger.debug("Did not recognise order_by parameter. Returning sets ordered by id (default)")
                return session.scalars(select(Set)
                                        .where(Set.tunestarter_id == self.id)
                                        .order_by(Set.id)).all()
    
    @classmethod
    def get_tunestarter(Tunestarter, id):
        logger.debug("Return tunestarter object for tunestarter with ID {}".format(id))
        with Session(db.get_engine()) as session:
            tunestarter = session.scalars(select(Tunestarter).where(Tunestarter.id == id)).first()
            return tunestarter