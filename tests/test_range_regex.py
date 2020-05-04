import unittest
from milk.util.range_regex import get_range_regex


class TestRangeRegex(unittest.TestCase):

  def test_range_regex(self):
    p = get_range_regex()
    self.assertEqual("A", p.match("A1:A1").group('startRow'))
    self.assertEqual("A", p.match("A1").group('startRow'))
    self.assertEqual(None, p.match("A1").group('endRow'))
    self.assertEqual("test", p.match("test!A1:A1").group('sheet'))
    self.assertEqual("AA", p.match("test!AA1:A1").group('startRow'))
    self.assertEqual("10", p.match("test!A1:A10").group('endColumn'))
