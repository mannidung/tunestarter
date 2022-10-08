import hashlib
import time
from .sources import *
from .db import *
import utils
import settings

from sqlalchemy import Column
from sqlalchemy import Integer, String
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

import os
import sjkabc
import urllib.request as request

Base = declarative_base()

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
                                self.abc,
                                self.label)

    def download(self):
        url = ""
        if self.source_id > 0:
            utils.debug_print("Downloading by ID")
            url = self.__url_from_ID()
        elif self.name != None:
            utils.debug_print("Downloading by name")
            url = self.__url_from_name()
        else:
            utils.debug_print("Not downloading")
            return
        temp_path = os.path.join(settings.settings["storage"],
                                    '{}_{}_{}.abc'.format(self.source, self.source_id, self.source_setting))
        # Check if file exists, in which case we don't need to download it
        exists = False
        if os.path.exists(temp_path):
            utils.debug_print("File with path {} already exists, setting tune.existing to True".format(temp_path))
            exists = True
        if not exists:
            # Download it
            utils.debug_print("File with path {} does not exist, downloading from url {}".format(temp_path, url))
            request.urlretrieve(url, temp_path)
            self.downloaded_timestamp = int(time.time())
            utils.debug_print("timestamp: {}".format(self.downloaded_timestamp))
            utils.debug_print("File at url {} downloaded to path {}.".format(temp_path, url))
        for tune in sjkabc.parse_file(temp_path):
            self.title = "".join(tune.title)
            self.rhythm = "".join(tune.rhythm)
            self.abc = "".join(tune.abc)
        self.label = hashlib.md5(open(temp_path,'rb').read()).hexdigest()
        
        
        
    def __url_from_ID(self):
        return get_source_url_by_id(self.source, self.source_id, self.source_setting)
    
    def __url_from_name(self):
        id = get_id_from_name(self.source, self.name)
        self.source_id = id
        return self.__url_from_ID()

"""  
def download(self):
        self.check_exists()
        if not self.exists:
            utils.debug_print("File with path {} does not exist, downloading from url {}".format(self.path, self.url))
            request.urlretrieve(self.url, self.path)
            utils.debug_print("File at url {} downloaded to path {}.".format(self.path, self.url))
            self.exists = True
    
    def get_metadata(self):
        if not self.check_exists():
            self.download()
        for tune in sjkabc.parse_file(self.path):
            self.title = "".join(tune.title)
            self.rhythm = "".join(tune.rhythm)
        self.label = hashlib.md5(open(self.path,'rb').read()).hexdigest()
        self.filename = os.path.join("tunes", self.rhythm, "{}.tex".format(self.label))
"""

def download_tunes():
    non_downloaded_tunes = select(Tune).where(Tune.downloaded_timestamp == None)
    with Session(get_engine()) as session:
        tunes = session.scalars(non_downloaded_tunes).all()
        for tune in tunes:
            tune.download()
        session.flush()
        session.commit()