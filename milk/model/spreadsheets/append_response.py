from milk.model.spreadsheets.update_values_response import UpdateValuesResponse


class AppendResponse():

  def __init__(
      self,
      spreadsheet_id: str,
      table_range: str,
      updates: UpdateValuesResponse
  ):
    self.spreadsheet_id = spreadsheet_id
    self.table_range = table_range
    self.updates = updates
