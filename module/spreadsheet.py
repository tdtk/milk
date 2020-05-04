from __future__ import print_function
import pickle
import os.path
import os
import json
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_RANGE_NAME = 'Class Data!A2:E'


def get_credentials():
  creds = None
  # The file token.pickle stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
      creds = pickle.load(token)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_config(json.loads(os.environ['SPREADSHEET_CREDENTIALS']), scopes=SCOPES)
      creds = flow.run_local_server(port=0)
  # Save the credentials for the next run
  with open('token.pickle', 'wb') as token:
    pickle.dump(creds, token)
  return creds


def record_money(usr_name: str, item_name: str, item_cost: int):
  service = build('sheet', 'v4', credentials=get_credentials())
  spreadsheet_id = os.environ['MILK_SPREADSHEET_ID']
  value_range_body = {
      "range": "A2:D2",
      "majorDimension": "ROWS",
      "values": [[datetime.date.today(), usr_name, item_name, item_cost]]
  }
  request = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=value_range_body['range'], body=value_range_body)
  response = request.execute()
  return response


def main():
  """Shows basic usage of the Sheets API.
  Prints values from a sample spreadsheet.
  """

  service = build('sheets', 'v4', credentials=get_credentials())

  # Call the Sheets API
  sheet = service.spreadsheets()
  result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                              range=SAMPLE_RANGE_NAME).execute()
  values = result.get('values', [])

  if not values:
    print('No data found.')
  else:
    print('Name, Major:')
    for row in values:
      # Print columns A and E, which correspond to indices 0 and 4.
      print('%s, %s' % (row[0], row[4]))


if __name__ == '__main__':
  main()
