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


def pay(args: list, event: MessageEvent, api: LineBotApi):
  if len(args) != 3:
    raise Exception(f'Number of args must be 3, not {len(args)}')
  profile = get_profile(event, api)
  service = SpreadsheetService()
  buyer = profile.display_name
  item = args[1]
  cost = args[2]
  try:
    service.append_purchase_data(buyer=buyer, item=item, cost=cost)
  except:
    try:
      service.add_this_month_sheet()
      service.append_purchase_data(buyer=buyer, item=item, cost=cost)
    except Exception as e:
      return f'支払い情報の登録に失敗しました。\n 詳細: {e}'
  return f'{buyer}さんの{item}の代金{cost}円を登録しました!'
