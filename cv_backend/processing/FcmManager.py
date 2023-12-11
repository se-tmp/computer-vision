import argparse
import json
import requests
import google.auth.transport.requests
from google.oauth2 import service_account
import os

PROJECT_ID = 'se-tmp'
BASE_URL = 'https://fcm.googleapis.com'
FCM_ENDPOINT = 'v1/projects/' + PROJECT_ID + '/messages:send'
FCM_URL = BASE_URL + '/' + FCM_ENDPOINT
SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']

class FcmManager:
    def _get_access_token(self):
        credentials
        if "IN_CONTAINER" not in os.environ:
            credentials = service_account.Credentials.from_service_account_file(
            '../se-tmp-pk.json', scopes=SCOPES)
        else:
            credentials = service_account.Credentials.from_service_account_file(
            '/run/secrets/fb_pk', scopes=SCOPES)
        request = google.auth.transport.requests.Request()
        credentials.refresh(request)
        return credentials.token

    def send_fcm_message(self, routineNumber: str):
        headers = {
            'Authorization': 'Bearer ' + self._get_access_token(),
            'Content-Type': 'application/json; UTF-8',
        }
        resp = requests.post(FCM_URL, data=json.dumps(self._build_message(routineNumber)), headers=headers)

        if resp.status_code == 200:
            print('Message sent to Firebase for delivery, response:')
            print(resp.text)
        else:
            print('Unable to send message to Firebase')
            print(resp.text)

    def _build_message(self, routineNumber):
        return {
            'message': {
                'topic': 'all',
                'data': {
                    'title': 'start routine',
                    'body': str(routineNumber)
                }
            }
        }
