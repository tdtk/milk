from linebot import (
  LineBotApi
)

def is_greeting(text: str):
  return text in ['こんにちは', 'おはよう', 'おやすみ', 'はじめまして']

def greeting(text: str, user_id: str, group_id, api: LineBotApi):
  if group_id:
    user_profile = api.get_group_member_profile(group_id, user_id)
  else:
    user_profile = api.get_profile(user_id)
  return f'{user_profile.display_name}さん! {text}😊'

