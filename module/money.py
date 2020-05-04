from linebot import (
    LineBotApi
)

from linebot.models import (
    MessageEvent
)

from module.util import (
    get_profile
)


def pay(args: list, event: MessageEvent, api: LineBotApi):
  if len(args) != 3:
    raise Exception(f'Number of args must be 3, not {len(args)}')
  profile = get_profile(event, api)
  return f'{profile.display_name}さんの{args[1]}の代金{args[2]}円を登録しました!'
