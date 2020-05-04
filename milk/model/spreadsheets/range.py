from milk.util.range_regex import get_range_regex


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
  def trancelate_row(row: int) -> str:
    row -= 1
    res = ''
    for i in range((row // 26) + 1):
      res += chr(65 + (row % 26))
    return res

  @staticmethod
  def retrancelate_row(row: str) -> int:
    res = 0
    for i, c in enumerate(row):
      res += ord(c) - 65 + i * 26
    return res + 1

  @classmethod
  def init_from_str(cls, range_: str):
    m = get_range_regex().match(range_)
    startRow = cls.retrancelate_row(m.group("startRow"))
    startColumn = int(m.group("startColumn"))
    endRow = cls.retrancelate_row(m.group("endRow")) if m.group("endRow") else startRow
    endColumn = int(m.group("endColumn")) if m.group("endColumn") else startColumn
    return cls(startRow, endRow, startColumn, endColumn, sheet=m.group("sheet"))

  def __str__(self):
    return f"{ self.sheet + '!' if self.sheet else ''}{self.trancelate_row(self.startRow)}{self.startColumn}:{self.trancelate_row(self.endRow)}{self.endColumn}"
