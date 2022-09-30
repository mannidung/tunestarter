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

def setup_db(path, debug=False):
    global _engine
    _engine = create_engine('sqlite:///{}'.format(path), echo = debug)
    if not database_exists(_engine.url):
        create_database(_engine.url)
    create_schema(_engine)

def create_schema(engine):
    metadata_obj = get_metadata()

    # Table containing sets.
    Table('sets', metadata_obj,
        Column('id', Integer, primary_key=True),
        Column('name', String, nullable=False, unique=True)
    )

    # Table containing sources, e.g. thesession, local, etc.
    Table('sources', metadata_obj,
        Column('id', Integer, primary_key=True),
        Column('name', String, nullable=False)
    )

    # The table containing the actual tunes and abc-data
    Table('tunes', metadata_obj,
        Column('id', Integer, primary_key=True),
        Column('name', String, nullable=False),
        Column('source', Integer, ForeignKey('sources.id')),
        Column('source_id', Integer, nullable=False),
        Column('source_setting', Integer, nullable=True),
        Column('title', String, nullable=False),
        Column('rhythm', String, nullable=False),
        Column('abc', String, nullable=False)
    )

    # The table containing the tunestarters
    Table('tunestarters', metadata_obj,
        Column('id', Integer, primary_key=True),
        Column('name', String, nullable=False, unique=True)
    )

    # Bridging table, tunestarters to sets
    Table('tunestarters_to_sets', metadata_obj,
        Column('tunestarter', Integer, nullable=False),
        Column('set', Integer, nullable=False),
        UniqueConstraint('tunestarter', 'set', name='unique_index_1')
    )

    # Bridging table, tunes to sets
    Table('tunes_to_sets', metadata_obj,
        Column('set', Integer, nullable=False),
        Column('tune', Integer, nullable=False),
        Column('order', Integer, nullable=False)
    )
    
    metadata_obj.create_all(engine)