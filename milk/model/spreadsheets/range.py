
class Range:
  def __init__(self, startRow: int, endRow: int, startColumn: int, endColumn: int, sheet=None):
    if (startRow == 0 or endRow == 0 or startColumn == 0 or endColumn == 0):
      raise Exception("Range of spreadsheets starts from 1")
    self.startRow = startRow
    self.endRow = endRow
    self.startColumn = startColumn
    self.endColumn = endColumn
    self.sheet = sheet

  @staticmethod
  def trancelate_row(row: int):
    row -= 1
    res = ''
    for i in range((row // 26) + 1):
      res += chr(65 + (row % 26))
    return res

  def __str__(self):
    return f"{ sheet + '!' if sheet else ''}"
