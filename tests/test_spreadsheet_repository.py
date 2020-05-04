import unittest
import os
from milk.repository.spreadsheet_repository import SpreadsheetRepository
from milk.model.spreadsheets.range import Range
from milk.model.spreadsheets.dimension import Dimension
from milk.model.spreadsheets.value_range import ValueRange
from milk.util.dotenv import load


class TestSpreadsheetRepository(unittest.TestCase):

  def setUp(self):
    load(path="../.env")
    self.repository = SpreadsheetRepository(os.environ['SPREADSHEET_CREDENTIALS'], os.environ['MILK_SPREADSHEET_ID'])

  def test_get(self):
    range_ = Range(1, 1, 1, 1, sheet="test")
    expect = ValueRange("test!A1", Dimension.ROWS, values=[["1"]])
    actual = self.repository.get(range_=range_, major_dimension=Dimension.ROWS)
    self.assertEqual(expect.values, actual.values)
    self.assertEqual(expect.range, actual.range)
    self.assertEqual(expect.major_dimension, actual.major_dimension)
