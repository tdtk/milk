from milk.model.spreadsheets.range import Range


class ClearResponse():
  def __init__(self, spreadsheet_id: str, cleared_range: Range):
    self.spreadsheet_id = spreadsheet_id
    self.cleared_range = cleared_range
