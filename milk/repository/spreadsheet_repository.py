from __future__ import print_function
import pickle
import os.path
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from milk.model.spreadsheets.range import Range
from milk.model.spreadsheets.dimension import Dimension
from milk.model.spreadsheets.value_render_option import ValueRenderOption
from milk.model.spreadsheets.date_time_render_option import DateTimeRenderOption
from milk.model.spreadsheets.value_range import ValueRange

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


class SpreadsheetRepository():

  def __init__(self, credentials, spreadsheet_id):
    self.credentials = credentials
    self.spreadsheet_id = spreadsheet_id

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

  def get(
          self,
          range_: Range,
          major_dimension=Dimension.DIMENSION_UNSPECIFIED,
          value_render_option=ValueRenderOption.FORMATTED_VALUE,
          date_time_render_option=DateTimeRenderOption.SERIAL_NUMBER) -> ValueRange:
    service = build('sheets', 'v4', credentials=self.get_credentials())
    request = service.spreadsheets().values().get(
        spreadsheetId=self.spreadsheet_id,
        range=range_,
        majorDimension=major_dimension.value,
        valueRenderOption=value_render_option.value,
        dateTimeRenderOption=date_time_render_option.value
    )
    response = request.execute()
    return ValueRange(response["range"], Dimension[response["majorDimension"]], response["values"])
