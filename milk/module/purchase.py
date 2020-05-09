from linebot import (
    LineBotApi
)

from linebot.models import (
    MessageEvent
)

from milk.module.util import (
    get_profile
)

from milk.service.spreadsheet_service import SpreadsheetService
import datetime


def pay(args: list, event: MessageEvent, api: LineBotApi):
  if len(args) != 3:
    raise Exception(f'Number of args must be 3, not {len(args)}')
  profile = get_profile(event, api)
  service = SpreadsheetService()
  buyer = profile.display_name
  item = args[1]
  cost = int(args[2])
  try:
    service.append_purchase_data(buyer=buyer, item=item, cost=cost)
  except:
    try:
      service.add_this_month_sheet()
      service.append_purchase_data(buyer=buyer, item=item, cost=cost)
    except Exception as e:
      return f'支払い情報の登録に失敗しました。\n 詳細: {e}'
  return f'{buyer}さんの{item}の代金{cost}円を登録しました!'


def get_total(args: list):
  if not(len(args) == 2 or len(args) == 3):
    raise Exception(f'Number of args must be 2 or 3, not {len(args)}')
  service = SpreadsheetService()
  month = int(args[1])
  year = int(dict(enumerate(args)).get(2, datetime.date.today().year))
  try:
    data = service.get_all_purchase_data(f"{year}/{month}")
    buyer2cost = {}
    buyer_list = []
    res = ""
    for d in data:
      if d.buyer in buyer2cost:
        buyer2cost[d.buyer] += d.cost
      else:
        buyer2cost[d.buyer] = 0
    for k, v in buyer2cost.items():
      buyer_list.append(k)
      res += f"{k}さんは{v}円の支払っています!\n"
    if len(buyer_list) == 2:
      if buyer2cost[buyer_list[0]] > buyer2cost[buyer_list[1]]:
        res += f"{buyer_list[1]}さんが{buyer_list[0]}さんに{buyer2cost[buyer_list[0]] - buyer2cost[buyer_list[1]]}円支払いましょう!"
      else:
        res += f"{buyer_list[0]}さんが{buyer_list[1]}さんに{buyer2cost[buyer_list[1]] - buyer2cost[buyer_list[0]]}円支払いましょう!"
    return res

  except:
    return "データの取得に失敗しました。"
