import json
import urllib2
import urllib
from feedback import Feedback

_DEFAULTHOST = "http://cvrapi.dk/api?country=dk&version=3"


def get_data(cvr):
    req = urllib2.Request(_DEFAULTHOST + "&search=" + urllib.quote(cvr))
    req.add_header("Accept", "application/json")
    req.add_header("User-agent", "CVR-Alfred")
    try:
        res = urllib2.urlopen(req)
        return json.loads(res.read())
    except urllib2.URLError:
        print "Kan ikke oprette forbindelse"
        raise SystemExit()


def parse_data(data, showCVR):
    fb = Feedback()
    address = data['address'] + ", " + str(data['zipcode']) + " " + data['city']
    name = data['name']
    phone = ""
    mail = ""
    if showCVR:
        name = data['name'] + " - " + str(data['vat'])
    if 'phone' in data:
            phone = " - Tlf: " + data['phone']
    if 'email' in data:
        mail = " - Email: " + data['email']
    fb.add_item(name, address + phone + mail, str(data['vat']))
    return fb


def lookup(query):
    fb = Feedback()
    if len(query) == 8 and query.isdigit():
        data = get_data(query)
        if 'error' in data:
            fb.add_item("Ugyldigt CVR-nummer")
        else:
            fb = parse_data(data, False)
    elif len(query) > 8 and query.isdigit():
        fb.add_item("CVR-nummeret er for langt", "CVR-numre er 8-cifret")
    elif len(query) < 8 and query.isdigit():
        fb.add_item("Indtast CVR-nummer")
    else:
        data = get_data(query)
        fb = parse_data(data, True)
    print fb
