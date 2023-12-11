# just for testing

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

class Firestore():
    def __init__(self):
        if "IN_CONTAINER" not in os.environ:
            self.cred = credentials.Certificate('../se-tmp-pk.json')
        else:
            self.cred = credentials.Certificate('/run/secrets/fb_pk')
        firebase_admin.initialize_app(self.cred)

        self.db = firestore.client()