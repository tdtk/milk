class PurchaseData:
  def __init__(self, date: str, buyer: str, item: str, cost: int):
    self.date = date
    self.buyer = buyer
    self.item = item
    self.cost = cost

  @classmethod
  def init_from_list(cls, l: list):
    return cls(l[0], l[1], l[2], l[3])
