

from tune import Tune
import os
import settings

def test_tune_init():
    settings.read_setup()

    for f in os.listdir(settings.settings["storage"]):
        if not f.endswith(".abc"):
            continue
        os.remove(os.path.join(settings.settings["storage"], f))

    # A tune generated with input should have that input as class variables
    t1 = Tune("thesession", 1, 2)
    assert t1.source == "thesession"
    assert t1.id == 1
    assert t1.setting == 2

    # A tune generated without setting input should have setting 1
    t2 = Tune("thesession", 1)
    assert t2.setting == 1

    # t1 and t2 should have URLs
    assert t1.url == "https://thesession.org/tunes/1/abc/2"
    assert t2.url == "https://thesession.org/tunes/1/abc/1"

    # t1 and t2 should have path None since the files aren't yet downloaded
    assert t1.path == os.path.join(settings.settings["storage"], 'thesession_{}_{}.abc'.format(t1.id, t1.setting))
    assert t2.path == os.path.join(settings.settings["storage"], 'thesession_{}_{}.abc'.format(t2.id, t2.setting))

def test_check_exists():
    settings.read_setup()
    for f in os.listdir(settings.settings["storage"]):
        if not f.endswith(".abc"):
            continue
        os.remove(os.path.join(settings.settings["storage"], f))
    t1 = Tune("thesession", 1, 2)
    assert t1.exists == False
    t1.download()
    assert t1.exists == True

    for f in os.listdir(settings.settings["storage"]):
        if not f.endswith(".abc"):
            continue
        os.remove(os.path.join(settings.settings["storage"], f))
    
    t1.check_exists()
    
    assert t1.exists == False

    t1.download()
    
    assert t1.exists == True


def test_tune_download():
    settings.read_setup()

    for f in os.listdir(settings.settings["storage"]):
        if not f.endswith(".abc"):
            continue
        os.remove(os.path.join(settings.settings["storage"], f))

    t1 = Tune("thesession", 4, 2)
    assert t1.path == os.path.join(settings.settings["storage"], 'thesession_{}_{}.abc'.format(t1.id, t1.setting))
    assert t1.exists == False
    
    t1.download()

    assert t1.exists == True

