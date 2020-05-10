from milk.repository.spreadsheet_repository import SpreadsheetRepository
from milk.model.spreadsheets.range import Range
from milk.model.spreadsheets.dimension import Dimension
from milk.model.spreadsheets.value_input_option import ValueInputOption
from milk.model.spreadsheets.value_range import ValueRange
import datetime
import os
from milk.model.purchase.purchase_data import PurchaseData


class SpreadsheetService:
  def __init__(self):
    self.repository = SpreadsheetRepository(os.environ['SPREADSHEET_CREDENTIALS'], os.environ['MILK_SPREADSHEET_ID'])

  def init_sheet(self, sheet: str):
    range_ = Range(1, 1, 4, 1, sheet=sheet)
    body = ValueRange(range_, Dimension.ROWS, values=[["date", "buyer", "item", "cost"]])
    self.repository.update(range_, body, ValueInputOption.RAW)

  def append_purchase_data(self, buyer: str, item: str, cost: int):
    today = datetime.date.today()
    sheet_name = f"{today.year}/{today.month}"
    range_ = Range(1, 2, 4, 2, sheet=sheet_name)
    body = ValueRange(range_, Dimension.ROWS, values=[[str(today), buyer, item, cost]])
    self.repository.append(range_, body, ValueInputOption.RAW)

  def add_this_month_sheet(self):
    today = datetime.date.today()
    sheet_name = f"{today.year}/{today.month}"
    self.repository.add_sheet(sheet_name)
    self.init_sheet(sheet_name)

  def get_all_purchase_data(self, sheet: str) -> ValueRange:
    range_ = Range(1, 2, 4, 100, sheet=sheet)
    v_range = self.repository.get(range_=range_, major_dimension=Dimension.ROWS)
    return list(map(lambda l: PurchaseData.init_from_list(l), v_range.values))

  def clear(self, sheet: str, column: int):
    range_ = Range(1, column, 4, column, sheet=sheet)
    self.repository.clear(range_)

  def get_sheet_url(self):
    return f"https://docs.google.com/spreadsheets/d/{os.environ['MILK_SPREADSHEET_ID']}/edit?usp=sharing"
