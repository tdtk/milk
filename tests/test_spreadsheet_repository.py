import unittest
import os
from milk.repository.spreadsheet_repository import SpreadsheetRepository
from milk.model.spreadsheets.range import Range
from milk.model.spreadsheets.dimension import Dimension
from milk.model.spreadsheets.value_range import ValueRange
from milk.model.spreadsheets.value_input_option import ValueInputOption
from milk.util.dotenv import load


class TestSpreadsheetRepository(unittest.TestCase):

  def setUp(self):
    load(path="../.env")
    self.repository = SpreadsheetRepository(os.environ['SPREADSHEET_CREDENTIALS'], os.environ['MILK_SPREADSHEET_ID'])

  def test_get(self):
    range_ = Range(1, 1, 1, 1, sheet="test")
    expect = ValueRange(Range.init_from_str("test!A1"), Dimension.ROWS, values=[[1]])
    actual = self.repository.get(range_=range_, major_dimension=Dimension.ROWS)
    self.assertEqual(expect.get_str_values(), actual.values)
    self.assertEqual(str(expect.range), str(actual.range))
    self.assertEqual(expect.major_dimension, actual.major_dimension)

  def test_append(self):
    range_ = Range(1, 3, 1, 3, sheet="test")
    body = ValueRange(range_, Dimension.ROWS, values=[[2]])
    response = self.repository.append(range_, body, ValueInputOption.RAW, include_values_in_response=True)
    self.assertEqual(body.get_str_values(), response.updates.updated_data.values)
    self.repository.clear(range_)

  def test_update(self):
    range_ = Range(1, 2, 1, 2, sheet="test")
    body = ValueRange(range_, Dimension.ROWS, values=[[3]])
    response = self.repository.update(range_, body, ValueInputOption.RAW, include_values_in_response=True)
    self.assertEqual(body.get_str_values(), response.updated_data.values)
