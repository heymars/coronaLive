from urllib.request import urlopen

from urllib.error import HTTPError

from urllib.error import URLError

import google
from bs4 import BeautifulSoup

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import jsonify
import string

import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    db = firestore.client()
    doc_ref = db.collection(u'corona').document(u'livedata')

    try:
        doc = doc_ref.get()
        print(u'Document data: {}'.format(doc.to_dict()))
        return jsonify(doc.to_dict())
    except google.cloud.exceptions.NotFound:
        return u'No such document!'


def add_data(total: object, death: object, recovered: object):
    db = firestore.client()

    doc_ref = db.collection(u'corona').document(u'livedata')
    doc_ref.set({
        u'total': total,
        u'death': death,
        u'recovered': recovered
    })


def initialize():
    cred = credentials.Certificate('/home/sujeett9l/PycharmProjects/coronaLive/serviceAccountKey.json')
    firebase_admin.initialize_app(cred)


try:

    html = urlopen("https://www.worldometers.info/coronavirus/")

except HTTPError as e:

    print(e)

except URLError:

    print("Server down or incorrect domain")

else:

    res = BeautifulSoup(html.read(), "html5lib")

    head = res.findAll("div", {"id": "maincounter-wrap"})
    initialize()
    my_list = []
    for h in head:
        s = h.getText()
        final_str = s.translate({ord(c): None for c in string.whitespace})
        my_list.append(final_str)
        print(h.getText())
add_data(total=my_list[0], death=my_list[1], recovered=my_list[2])

app.run()
