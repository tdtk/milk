import unittest
import datetime
from milk.service.spreadsheet_service import SpreadsheetService
from milk.util.dotenv import load


class TestSpreadsheetService(unittest.TestCase):

  def setUp(self):
    load(path="../.env")
    self.service = SpreadsheetService()

  def test_append_data(self):
    try:
      self.service.append_purchase_data(buyer="test", item="test", cost=0)
    except:
      self.service.add_this_month_sheet()
      self.service.append_purchase_data(buyer="test", item="test", cost=0)

  def test_get_all_purchase_data(self):
    today = datetime.date.today()
    sheet_name = f"{today.year}/{today.month}"
    response = self.service.get_all_purchase_data(sheet_name)
    print(response)
