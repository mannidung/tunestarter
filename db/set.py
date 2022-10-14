from db.tune import Tune
from .db import *
import logging

from sqlalchemy import Column
from sqlalchemy import Integer, String
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger(__name__)

Base = declarative_base()

class Set(Base):
    __tablename__ = 'sets'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    title = Column(String)
    rhythm = Column(String)
    tunestarter_id = Column(Integer)
    
    def __repr__(self):
        return "\n\t---\n\t"\
                "ID: {} \n\t"\
                "Name: {}\n\t"\
                "Title: {}\n\t"\
                "Rhythm: {}\n\t"\
                "Tunestarter_id: {}\n\t"\
                "---\n".format(self.id,
                                self.name,
                                self.title,
                                self.rhythm,
                                self.tunestarter_id,
                                )
    
    def tunes(self):
        tunes_to_sets_table = get_metadata().tables['tunes_to_sets']
        with Session(get_engine()) as session:
            #set = session.scalars(select(Set).where(Set.id == id)).first()
            result = session.execute(select(tunes_to_sets_table)
                                    .where(tunes_to_sets_table.c.set == self.id)
                                    .order_by(tunes_to_sets_table.c.order))
            tunes = []
            for row in result:
                tunes.append(session.scalars(select(Tune).where(Tune.id == row[1])).first())
            return tunes
    
    def set_title(self):
        with Session(get_engine()) as session:
            session.add(self)
            logger.debug("Setting title of set {}".format(self.id))
            if "TMP" not in self.name:
                logger.debug("Set.Name {} seems to specified by user, keeping as title")
                self.title = self.name
            else:
                logger.debug("Set.Name not set by user, creating title from tune names")
                tune_titles = []
                tunes = self.tunes()
                for tune in tunes:
                    tune_titles.append(tune.title)
                self.title = ' | '.join(tune_titles)
                logger.debug("Set {} now has title {}".format(self.id, self.title))

            #setattr(self, 'title', self.title)
            logger.debug("Saving rhythm to database")
            
            session.commit()
    
    def set_rhythm(self):
        logger.debug("Setting rhythm of set {}".format(self.id))
        tunes = self.tunes()
        index = 0
        rhythm = ""
        for tune in tunes:
            if index == 0:
                logger.debug("First tune has rhythm {}".format(tune.rhythm))
                rhythm = tune.rhythm
            else:
                if rhythm != tune.rhythm:
                    logger.debug("One of the tunes differ in rhythm, has rhythm {}. Setting rhythm to mixed".format(tune.rhythm))
                    rhythm = "mixed"
                    break
            index = index + 1
        logger.debug("Set rhythm is {}".format(rhythm))
        setattr(self, 'rhythm', rhythm)
        #self.rhythm = rhythm
        with Session(get_engine()) as session:
            logger.debug("Saving rhythm to database")
            session.add(self)
            session.commit()

def prepare_sets(tunestarter_id):
    sets = get_sets(tunestarter_id)
    for set in sets:
        set.set_rhythm()
        set.set_title()

def get_set(id):
    with Session(get_engine()) as session:
        set = session.scalars(select(Set).where(Set.id == id)).first()
        #print(set)
        return set

def get_sets(tunestarter_id):
    with Session(get_engine()) as session:
        sets = session.scalars(select(Set).where(Set.tunestarter_id == tunestarter_id)).all()
        return sets