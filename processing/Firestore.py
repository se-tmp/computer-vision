# just for testing

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class Firestore():
    def __init__(self):
        self.cred = credentials.Certificate('se-tmp-pk.json')
        firebase_admin.initialize_app(self.cred)

        self.db = firestore.client()