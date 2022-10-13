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

def test():
    set = get_set(1)
    tunes = set.tunes()
    for tune in tunes:
        print(tune)

def get_set(id):
    with Session(get_engine()) as session:
        set = session.scalars(select(Set).where(Set.id == id)).first()
        #print(set)
        return set