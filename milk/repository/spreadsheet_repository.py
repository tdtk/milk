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
from milk.model.spreadsheets.value_input_option import ValueInputOption
from milk.model.spreadsheets.insert_data_option import InsertDataOption
from milk.model.spreadsheets.append_response import AppendResponse
from milk.model.spreadsheets.update_values_response import UpdateValuesResponse

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


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
    return ValueRange(Range.init_from_str(response["range"]), Dimension[response["majorDimension"]], response["values"])

  def append(
      self,
      range_: Range,
      body: ValueRange,
      value_input_option: ValueInputOption,
      insert_data_option=InsertDataOption.OVERWRITE,
      include_values_in_response=False,
      response_value_render_option=ValueRenderOption.FORMATTED_VALUE,
      response_date_time_render_option=DateTimeRenderOption.SERIAL_NUMBER
  ) -> AppendResponse:
    service = build('sheets', 'v4', credentials=self.get_credentials())
    request = service.spreadsheets().values().append(
        spreadsheetId=self.spreadsheet_id,
        range=str(range_),
        body={
            "range": str(body.range),
            "majorDimension": body.major_dimension.value,
            "values": body.values
        },
        valueInputOption=value_input_option.value,
        insertDataOption=insert_data_option.value,
        includeValuesInResponse=include_values_in_response,
        responseValueRenderOption=response_value_render_option.value,
        responseDateTimeRenderOption=response_date_time_render_option.value
    )
    response = request.execute()
    updates = response["updates"]
    updated_data = None
    if ("updatedData" in updates):
      updated_data = updates["updatedData"]
      updated_data = ValueRange(
          range_=updated_data["range"],
          major_dimension=updated_data["majorDimension"],
          values=updated_data["values"]
      )
    return AppendResponse(
        spreadsheet_id=response["spreadsheetId"],
        table_range=response["tableRange"],
        updates=UpdateValuesResponse(
            spreadsheet_id=updates["spreadsheetId"],
            updated_range=updates["updatedRange"],
            updated_rows=updates["updatedRows"],
            updated_columns=updates["updatedColumns"],
            updated_cells=updates["updatedCells"],
            updated_data=updated_data
        )
    )

  def update(
      self,
      range_: Range,
      body: ValueRange,
      value_input_option: ValueInputOption,
      include_values_in_response=False,
      response_value_render_option=ValueRenderOption.FORMATTED_VALUE,
      response_date_time_render_option=DateTimeRenderOption.SERIAL_NUMBER
  ) -> UpdateValuesResponse:
    service = build('sheets', 'v4', credentials=self.get_credentials())
    request = service.spreadsheets().values().update(
        spreadsheetId=self.spreadsheet_id,
        range=str(range_),
        body={
            "range": str(body.range),
            "majorDimension": body.major_dimension.value,
            "values": body.values
        },
        valueInputOption=value_input_option.value,
        includeValuesInResponse=include_values_in_response,
        responseValueRenderOption=response_value_render_option.value,
        responseDateTimeRenderOption=response_date_time_render_option.value
    )
    response = request.execute()
    updated_data = None
    if ("updatedData" in response):
      updated_data = response["updatedData"]
      updated_data = ValueRange(
          range_=updated_data["range"],
          major_dimension=updated_data["majorDimension"],
          values=updated_data["values"]
      )
    return UpdateValuesResponse(
        spreadsheet_id=response["spreadsheetId"],
        updated_range=response["updatedRange"],
        updated_rows=response["updatedRows"],
        updated_columns=response["updatedColumns"],
        updated_cells=response["updatedCells"],
        updated_data=updated_data
    )
