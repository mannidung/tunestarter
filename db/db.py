from enum import unique
from sqlalchemy import create_engine
from sqlalchemy import MetaData, select
from sqlalchemy import Table, Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy_utils import database_exists, create_database

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
    _engine = create_engine('sqlite:///{}'.format(path), echo = debug)
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
        Column('id', Integer, primary_key=True),
        Column('name', String, nullable=False),
        Column('tunestarter_id', Integer, ForeignKey('tunestarters.id')),
        UniqueConstraint('name', 'tunestarter_id', name='unique_index_tunestarterstosets')
    )

    # Table containing sources, e.g. thesession, local, etc.
    Table('sources', metadata_obj,
        Column('id', Integer, primary_key=True),
        Column('name', String, nullable=False, unique=True)
    )

    # The table containing the actual tunes and abc-data
    Table('tunes', metadata_obj,
        Column('id', Integer, primary_key=True),
        Column('name', String, nullable=False),
        Column('source', Integer, ForeignKey('sources.id')),
        Column('source_id', Integer, nullable=False),
        Column('source_setting', Integer, nullable=False),
        Column('downloaded_timestamp', Integer, nullable=True), # Downloaded timestamp in unix time
        Column('title', String, nullable=True),
        Column('rhythm', String, nullable=True),
        Column('abc', String, nullable=True),
        Column('label', String, nullable=True),
        UniqueConstraint('name',
                        'source',
                        'source_id',
                        'source_setting',
                        name='unique_index_tunes')
    )

    # The table containing the tunestarters
    Table('tunestarters', metadata_obj,
        Column('id', Integer, primary_key=True),
        Column('name', String, nullable=False, unique=True)
    )


    # Bridging table, tunes to sets
    Table('tunes_to_sets', metadata_obj,
        Column('set', Integer, nullable=False),
        Column('tune', Integer, nullable=False),
        Column('order', Integer, nullable=False)
        #UniqueConstraint('tunestarter', 'set', name='unique_index_tunestarterstosets')
    )
    
    metadata_obj.create_all(engine)