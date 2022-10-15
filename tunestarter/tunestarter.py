import hashlib
import time
import db
import logging
import sources
import settings
import sjkabc

import os

from sqlalchemy import Column
from sqlalchemy import Integer, String
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

from urllib import request

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
        
    def get_tunes(self):
        tunes = []
        tunes_table = db.get_metadata().tables['tunes']
        sets_table = db.get_metadata().tables['sets']
        tunes_to_sets_table = db.get_metadata().tables['tunes_to_sets']
        with Session(db.get_engine()) as session:
            # Get the 
            result = session.execute(select(tunes_table.c.id)
                                    .join_from(tunes_table, tunes_to_sets_table)
                                    .join_from(tunes_to_sets_table, sets_table)
                                    .where(sets_table.c.tunestarter_id == self.id)
                                    .order_by(tunes_table.c.rhythm, tunes_table.c.title)
                                    )
            already_appended = []
            for tune_id in result:
                if tune_id[0] not in already_appended:
                    tunes.append(Tune.get_tune(tune_id[0]))
                already_appended.append(tune_id[0])
        return tunes
        

    @classmethod
    def get_tunestarter(Tunestarter, id):
        logger.debug("Return tunestarter object for tunestarter with ID {}".format(id))
        with Session(db.get_engine()) as session:
            tunestarter = session.scalars(select(Tunestarter).where(Tunestarter.id == id)).first()
            return tunestarter

class Tune(Base):
    __tablename__ = 'tunes'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    source = Column(Integer)
    source_id = Column(Integer)
    source_setting = Column(Integer)
    downloaded_timestamp = Column(Integer)
    title = Column(String)
    rhythm = Column(String)
    transcription = Column(String)
    metre = Column(String)
    note_length = Column(String)
    key = Column(String)
    abc = Column(String)
    label = Column(String)


    def __repr__(self):
        return "\n\t---\n\t"\
                "ID: {} \n\t"\
                "Name: {}\n\t"\
                "Source: {}\n\t"\
                "Source_id: {}\n\t"\
                "Source_setting: {}\n\t"\
                "Downloaded_timestamp: {}\n\t"\
                "Title: {}\n\t"\
                "Rhythm: {}\n\t"\
                "Transcription: {}\n\t"\
                "Metre: {}\n\t"\
                "Note Length: {}\n\t"\
                "Key: {}\n\t"\
                "ABC: {}\n\t"\
                "Label: {}\n\t"\
                "---\n".format(self.id,
                                self.name,
                                self.source,
                                self.source_id,
                                self.source_setting,
                                self.downloaded_timestamp,
                                self.title,
                                self.rhythm,
                                self.transcription,
                                self.metre,
                                self.note_length,
                                self.key,
                                self.abc,
                                self.label)

    def download(self):
        logger.debug("Starting download of tune with name {}, id {}, setting {}".format(
                                                                                        self.name,
                                                                                        self.source_id,
                                                                                        self.source_setting))
        url = ""
        if self.source_id > 0:
            logger.debug("Downloading by ID")
            url = self.__url_from_ID()
        elif self.name != None:
            logger.debug("Downloading by name")
            url = self.__url_from_name()
        else:
            logger.debug("Not downloading")
            return
        temp_path = self.__get_temp_path()
        # Check if file exists, in which case we don't need to download it
        exists = False
        if os.path.exists(temp_path):
            logger.debug("File with path {} already exists, setting tune.existing to True".format(temp_path))
            exists = True
        if not exists:
            # Download it
            logger.debug("File with path {} does not exist, downloading from url {}".format(temp_path, url))
            request.urlretrieve(url, temp_path)
            self.downloaded_timestamp = int(time.time())
            logger.debug("timestamp: {}".format(self.downloaded_timestamp))
            logger.debug("File at url {} downloaded to path {}.".format(temp_path, url))
        self.__parse_abc(temp_path)
        self.label = hashlib.md5(open(temp_path,'rb').read()).hexdigest()
    
    def __parse_abc(self, path):
        for tune in sjkabc.parse_file(path):
            self.title = "".join(tune.title)
            self.rhythm = "".join(tune.rhythm)
            self.transcription = "".join(tune.transcription)
            self.metre = "".join(tune.metre)
            self.note_length = "".join(tune.note_length)
            self.key = "".join(tune.key)
            self.abc = "\n".join(tune.abc)

    def __get_temp_path(self):
        return os.path.join(settings.settings["storage"],
                                    '{}_{}_{}.abc'.format(self.source, self.source_id, self.source_setting))
        
    def __url_from_ID(self):
        return sources.get_source_url_by_id(self.source, self.source_id, self.source_setting)
    
    def __url_from_name(self):
        # Check if name already exists in database
        with Session(db.get_engine()) as session:
            tune = session.scalars(select(Tune).where(Tune.name == self.name)).first()
            if tune == None:
                logger.debug("Tune {} not found in database, will try to get id from name...".format(self.name))
                # Tune is not in database
                self.source_id = sources.get_id_from_name(self.source, self.name)
            else:
                # Tune is in database
                # If downloaded timestamp is None, then it hasn't been downloaded.
                # We need to get id from name and download it
                if tune.downloaded_timestamp == None:
                    logger.debug("Tune {} found in database but isn't downloaded, will try to download".format(self.name))
                    self.source_id = sources.get_id_from_name(self.source, self.name)
                
        return self.__url_from_ID()
    
    def get_sets(self):
        logger.debug("Getting sets where tune {} is included".format(self.id))
        sets = []
        tunes_table = db.get_metadata().tables['tunes']
        sets_table = db.get_metadata().tables['sets']
        tunes_to_sets_table = db.get_metadata().tables['tunes_to_sets']
        with Session(db.get_engine()) as session:
            # Get the 
            result = session.execute(select(tunes_to_sets_table.c.set)
                                    .join_from(tunes_table, tunes_to_sets_table)
                                    .join_from(tunes_to_sets_table, sets_table)
                                    .where(tunes_to_sets_table.c.tune == self.id)
                                    .order_by(sets_table.c.title)
                                    )
            for set_id in result:
                sets.append(Set.get_set(set_id[0]))
        return sets

    @classmethod
    def download_tunes(Tune):
        logger.debug("Starting downloading of tunes ####")
        with Session(db.get_engine()) as session:
            non_downloaded_tunes = select(Tune).where(Tune.downloaded_timestamp == None)
            tunes = session.scalars(non_downloaded_tunes).all()
            for tune in tunes:
                tune.download()
            session.flush()
            session.commit()
    
    @classmethod
    def get_tune(Tune, id):
        with Session(db.get_engine()) as session:
            Tune = session.scalars(select(Tune).where(Tune.id == id)).first()
            return Tune

class Set(Base):
    __tablename__ = 'sets'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    label = Column(String)
    title = Column(String)
    rhythm = Column(String)
    tunestarter_id = Column(Integer)
    
    def __repr__(self):
        return "\n\t---\n\t"\
                "ID: {} \n\t"\
                "Name: {}\n\t"\
                "Label: {}\n\t"\
                "Title: {}\n\t"\
                "Rhythm: {}\n\t"\
                "Tunestarter_id: {}\n\t"\
                "---\n".format(self.id,
                                self.name,
                                self.label,
                                self.title,
                                self.rhythm,
                                self.tunestarter_id,
                                )
    
    def tunes(self):
        tunes_to_sets_table = db.get_metadata().tables['tunes_to_sets']
        with Session(db.get_engine()) as session:
            #set = session.scalars(select(Set).where(Set.id == id)).first()
            result = session.execute(select(tunes_to_sets_table)
                                    .where(tunes_to_sets_table.c.set == self.id)
                                    .order_by(tunes_to_sets_table.c.order))
            tunes = []
            for row in result:
                tunes.append(session.scalars(select(Tune).where(Tune.id == row[1])).first())
            return tunes

    def prepare_set(self):
        self.set_label()
        self.set_rhythm()
        self.set_title()

    def set_label(self):
        with Session(db.get_engine()) as session:
            session.add(self)
            hash_string = self.name + str(self.id)
            self.label = hashlib.md5(hash_string.encode('utf-8')).hexdigest()
            session.commit()

    def set_title(self):
        with Session(db.get_engine()) as session:
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
        with Session(db.get_engine()) as session:
            session.add(self)
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
            logger.debug("Saving rhythm to database")
            session.commit()

    @classmethod
    def get_set(Set, id):
        with Session(db.get_engine()) as session:
            set = session.scalars(select(Set).where(Set.id == id)).first()
            #print(set)
            return set
