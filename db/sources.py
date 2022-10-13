from .db import *
import requests
import logging

logger = logging.getLogger(__name__)

def get_source_name_from_id(source):
    sources_table = get_metadata().tables['sources']
    source = sources_table.select().where(sources_table.c.id == source)
    result = get_connection().execute(source).first()
    return result[1]

def get_id_from_name(source, name):
    source_name = get_source_name_from_id(source)
    if source_name == "thesession":
        id = get_thesession_id_from_name(name)
        logger.debug("Source is thesession, found id {} from name {}".format(id, name))
        return id
    else:
        print("ERROR: source name wrong, no predefined source called {}".format(source_name))
        quit()

def get_source_url_by_id(source, source_id, source_setting):
    source_name = get_source_name_from_id(source)
    if source_name == "thesession":
        url = get_thesession_url(source_id, source_setting)
        logger.debug("Source is thesession, setting url to {}".format(url))
    else:
        print("ERROR: source name wrong, no predefined source called {}".format(source_name))
        quit()
    return url
    
def get_thesession_url(id, setting):
    if setting > 0:
        return 'https://thesession.org/tunes/{}/abc/{}'.format(id, setting)
    else:
        return 'https://thesession.org/tunes/{}/abc/1'.format(id, setting)

def get_thesession_id_from_name(name):
    # Name is specified, time to search...
    params = dict(
                q=name,
                format='json',
                perpage='1'
            )
    url = "https://thesession.org/tunes/search"

    resp = requests.get(url=url, params=params)
    data = resp.json() # Check the JSON Response Content documentation below
    if len(data["tunes"]) == 0:
        # No result was returned, search term needs to be improved
        print("ERROR: No search result for tune with name {}, please check the search terms".format(name))
        quit()
    id = data["tunes"][0]["id"]
    logger.debug("Tune found for name {}, using id {}".format(name, id))
    return id