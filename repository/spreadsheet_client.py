from __future__ import print_function
import pickle
import os.path
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


class SpreadsheetRepository():

  def _init_(self, credentials, spreadsheet_id):
    self.credentials = credentials
    self.spreadsheet_id = spreadsheet_id
    return self

  def get_credentials(self):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens,
    # and is created automatically when the authorization flow completes for the
    # first time.
    if os.path.exists('token.pickle'):
      with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_config(
            json.loads(self.credentials), scopes=SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
      pickle.dump(creds, token)
    return creds
