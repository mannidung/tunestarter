import hashlib
import time
from sources import *
import db
import settings
import logging

from sqlalchemy import Column
from sqlalchemy import Integer, String
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

import os
import sjkabc
import urllib.request as request

Base = declarative_base()
logger = logging.getLogger(__name__)

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
        return get_source_url_by_id(self.source, self.source_id, self.source_setting)
    
    def __url_from_name(self):
        # Check if name already exists in database
        with Session(db.get_engine()) as session:
            tune = session.scalars(select(Tune).where(Tune.name == self.name)).first()
            if tune == None:
                logger.debug("Tune {} not found in database, will try to get id from name...".format(self.name))
                # Tune is not in database
                self.source_id = get_id_from_name(self.source, self.name)
            else:
                # Tune is in database
                # If downloaded timestamp is None, then it hasn't been downloaded.
                # We need to get id from name and download it
                if tune.downloaded_timestamp == None:
                    logger.debug("Tune {} found in database but isn't downloaded, will try to download".format(self.name))
                    self.source_id = get_id_from_name(self.source, self.name)
                
        return self.__url_from_ID()

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