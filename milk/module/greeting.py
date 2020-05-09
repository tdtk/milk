from linebot import (
    LineBotApi
)

from linebot.models import (
    MessageEvent
)

from milk.module.util import (
    get_profile
)


def is_greeting(text: str):
  return text in ['こんにちは', 'おはよう', 'おやすみ', 'はじめまして']


def greeting(text: str, event: MessageEvent, api: LineBotApi):
  profile = get_profile(event, api)
  return f'{profile.display_name}さん! {text}😊'
