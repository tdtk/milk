from milk.model.spreadsheets.range import Range
from milk.model.spreadsheets.dimension import Dimension


class ValueRange():
  def __init__(self, range_: Range, major_dimension: Dimension, values: list):
    self.range = range_
    self.major_dimension = major_dimension
    self.values = values

  def get_str_values(self):
    return list(map(lambda ee: list(map(lambda e: str(e), ee)), self.values))
