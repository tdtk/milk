
from linebot import (
    LineBotApi
)

from linebot.models import (
    MessageEvent
)


def get_profile(event: MessageEvent, api: LineBotApi):
  source = event.source
  if hasattr(source, 'group_id'):
    return api.get_group_member_profile(source.group_id, source.user_id)
  else:
    return api.get_profile(source.user_id)
