from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy_utils import database_exists, create_database
import logging

logger = logging.getLogger(__name__)

_connection = None
_engine = None
_metadata = None

def get_connection():
    global _connection
    if not _connection:
        _connection = _engine.connect()
    return _connection

def get_metadata():
    global _metadata
    if not _metadata:
        _metadata = MetaData()
    return _metadata

def get_engine():
    global _engine
    return _engine

def setup_db(path, debug=False):
    global _engine
    _engine = create_engine('sqlite:///{}'.format(path), echo = False)
    if not database_exists(_engine.url):
        create_database(_engine.url)
    create_schema(_engine)
    setup_sources()

def setup_sources():
    predefined_sources = ["thesession"]
    sources_table = get_metadata().tables['sources']
    for source in predefined_sources:
        ins = sources_table.insert().values(name = source)
        try:
            get_connection().execute(ins)
            return
        except:
            return

def create_schema(engine):
    metadata_obj = get_metadata()

    # Table containing sets.
    Table('sets', metadata_obj,
        Column('id', Integer, primary_key=True), # Primary key
        Column('name', String, nullable=False), # Name of the set given in yaml
        Column('label', String, nullable=True), # Label of set, used for referencing in Latex
        Column('title', String, nullable=True), # Proper title of the set, either the same as the yaml, or generated from tune titles
        Column('rhythm', String, nullable=True), # Proper title of the set, either the same as the yaml, or generated from tune titles
        Column('tunestarter_id', Integer, ForeignKey('tunestarters.id')), # What tunestarter the set belongs to
        UniqueConstraint('name', 'tunestarter_id', name='unique_index_sets')
    )

    # Table containing sources, e.g. thesession, local, etc.
    Table('sources', metadata_obj,
        Column('id', Integer, primary_key=True),
        Column('name', String, nullable=False, unique=True)
    )

    # The table containing the actual tunes and abc-data
    Table('tunes', metadata_obj,
        Column('id', Integer, primary_key=True), # Primary key
        Column('name', String, nullable=False), # Name given in yaml file, used for search
        Column('source', Integer, ForeignKey('sources.id')), # ID of source for file, e.g. thesession
        Column('source_id', Integer, nullable=False), # ID of tune at the source
        Column('source_setting', Integer, nullable=False), # Setting of the tune at the source
        Column('downloaded_timestamp', Integer, nullable=True), # Downloaded timestamp in unix time
        Column('title', String, nullable=True), # Proper title of tune, from abc notation, ABC Key T
        Column('rhythm', String, nullable=True), # The rhythm (reel, jig, waltz, etc.) is it? ABC Key R
        Column('transcription', String, nullable=True), # Source of transcription, ABC Key Z
        Column('metre', String, nullable=True), # ABC Key M
        Column('note_length', String, nullable=True), # ABC key L
        Column('key', String, nullable=True), # ABC Key K
        Column('abc', String, nullable=True), # The abc notation
        Column('label', String, nullable=True), # Label, used for referencing in latex
        UniqueConstraint('name',
                        'source',
                        'source_id',
                        'source_setting',
                        name='unique_index_tunes') # Uniqueness constraint
    )
    # The table containing the tunestarters
    Table('tunestarters', metadata_obj,
        Column('id', Integer, primary_key=True),
        Column('name', String, nullable=False, unique=True)
    )


    # Bridging table, tunes to sets
    Table('tunes_to_sets', metadata_obj,
        Column('set', Integer, ForeignKey('sets.id'), nullable=False),
        Column('tune', Integer, ForeignKey('tunes.id'), nullable=False),
        Column('order', Integer, nullable=False),
        UniqueConstraint('set', 'tune', 'order', name='unique_index_tunestarterstosets')
    )
    
    metadata_obj.create_all(engine)