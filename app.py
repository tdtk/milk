import os
from flask import Flask, request, abort
import datetime

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, PostbackAction, PostbackEvent, TemplateSendMessage, ButtonsTemplate
)

from milk.module.greeting import is_greeting, greeting
from milk.module.purchase import pay, get_total, get_latest_data, clear_purchase_data, get_total_until_date
from milk.util.handle_action import action_data2dict
from milk.module.rich_menu import milk_rich_menu

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

rich_menu_id = line_bot_api.create_rich_menu(rich_menu=milk_rich_menu)

with open("./image/milk-rich-menu.png", "rb") as f:
  line_bot_api.set_rich_menu_image(rich_menu_id, "image/png", f)
  line_bot_api.set_default_rich_menu(rich_menu_id)


@app.route("/callback", methods=['POST'])
def callback():
  # get X-Line-Signature header value
  signature = request.headers['X-Line-Signature']

  # get request body as text
  body = request.get_data(as_text=True)
  # app.logger.info("Request body: " + body)

  # handle webhook body
  try:
    handler.handle(body, signature)
  except InvalidSignatureError:
    print("Invalid signature. Please check your channel access token/channel secret.")
    abort(400)

  return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
  text = event.message.text
  if is_greeting(text):
    text = greeting(text, event, line_bot_api)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
    return
  if text.startswith('みるく'):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text[4:]))
    return
  if text.startswith('支払い'):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=pay(text.split(), event, line_bot_api)))
    return
  if text.startswith("決算"):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=get_total(text.split())))
    return
  if text.startswith("ミス") or text.startswith("みす"):
    try:
      res = get_latest_data()
      line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
          alt_text="This is confirmation of clear latest purchase data",
          template=ButtonsTemplate(
              text=res["message"],
              title="最新の購入履歴を削除",
              actions=[
                  PostbackAction(
                    label="はい",
                    data=f"action=clear&sheet={res['sheet']}&index={res['index']}"
                  ),
                  PostbackAction(
                      label="いいえ",
                      data="action=cancel"
                  )
              ]
          )
      ))
    except Exception as e:
      line_bot_api.reply_message(event.reply_token, TextSendMessage(text=e))


@handler.add(PostbackEvent)
def handle_postback(event):
  data = action_data2dict(event.postback.data)
  if data["action"] == "cancel":
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="キャンセルしました!"))
  if data["action"] == "clear":
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=clear_purchase_data(data["sheet"], int(data["index"]))))
  if data["action"] == "calc_month":
    line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
        text=get_total_until_date(datetime.date.fromisoformat(event.postback.params["date"]))))


if __name__ == "__main__":
  port = int(os.getenv("PORT", 8000))
  app.run(host="0.0.0.0", port=port)
