from linebot import (
  LineBotApi
)

def is_greeting(text: str):
  return text in ['こんにちは', 'おはよう', 'おやすみ', 'はじめまして']

def greeting(text: str, user_id: str, api: LineBotApi):
  user_name = api.get_profile(user_id)
  return f'{user_name}さん! {text}😊'

