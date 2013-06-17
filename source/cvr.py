import json
import urllib2
from feedback import Feedback

_DEFAULTHOST = "https://cvrapi.dk/"


def url(cvr):
    return _DEFAULTHOST + cvr


def get_data(cvr):
    fb = Feedback()
    if len(cvr) == 8:
        req = urllib2.Request(url(cvr))
        req.add_header("Accept", "application/json")
        req.add_header("User-agent", "CVR-Alfred")
        try:
            res = urllib2.urlopen(req)
        except urllib2.URLError:
            print "Kan ikke oprette forbindelse"
            raise SystemExit()

        data = json.loads(res.read())

        if 'error' in data:
            fb.add_item("Ugyldigt CVR-nummer")
        else:
            address = data['adresse'] + ", " + str(data['postnr']) + " " + data['by']
            fb.add_item(data['navn'],  address + " - Tlf: " + data['telefon'], cvr)
    elif len(cvr) > 8:
        fb.add_item("CVR-nummeret er for langt", "CVR-numre er 8-cifret")
    else:
        fb.add_item("Indtast CVR-nummer")
    print fb
