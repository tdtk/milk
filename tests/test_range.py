import unittest
from milk.model.spreadsheets.range import Range


class TestRange(unittest.TestCase):

  def test_trancelate_row(self):
    self.assertEqual("A", Range.trancelate_row(1))
    self.assertEqual("AA", Range.trancelate_row(27))

  def test_retrancerate(self):
    self.assertEqual(1, Range.retrancelate_row("A"))
    self.assertEqual(27, Range.retrancelate_row("AA"))

  def test_range(self):
    range1 = Range(1, 1, 1, 1, sheet="Sheet1")
    self.assertEqual("Sheet1!A1:A1", str(range1))
    range2 = Range.init_from_str("Sheet1!A1:A1")
    self.assertEqual("Sheet1!A1:A1", str(range2))
    range3 = Range.init_from_str("Sheet1!A1")
    self.assertEqual("Sheet1!A1:A1", str(range2))
    range3 = Range.init_from_str("A1")
    self.assertEqual("A1:A1", str(range3))
