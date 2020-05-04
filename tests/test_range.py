import unittest
from milk.model.spreadsheets.range import Range


class TestRange(unittest.TestCase):

  def test_trancelate_row(self):
    self.assertEqual("A", Range.trancelate_row(1))
    self.assertEqual("AA", Range.trancelate_row(27))
    range1 = Range(1, 1, 1, 1, sheet="Sheet1")
    self.assertEqual("Sheet1!A1:A1", str(range1))
