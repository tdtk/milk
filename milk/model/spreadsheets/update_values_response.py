from milk.model.spreadsheets.value_range import ValueRange


class UpdateValuesResponse():
  def __init__(
      self,
      spreadsheet_id: str,
      updated_range: str,
      updated_rows: int,
      updated_columns: int,
      updated_cells: int,
      updated_data: ValueRange
  ):
    self.spreadsheet_id = spreadsheet_id
    self.updated_range = updated_range
    self.updated_rows = updated_rows
    self.updated_columns = updated_columns
    self.updated_cells = updated_cells
    self.updated_data = updated_data
