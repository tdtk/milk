from linebot import (
  LineBotApi
)

def is_greeting(text: str):
  return text in ['こんにちは', 'おはよう', 'おやすみ', 'はじめまして']

def greeting(text: str, user_id: str, api: LineBotApi):
  user_profile = api.get_profile(user_id)
  return f'{user_profile.display_name}さん! {text}😊'

