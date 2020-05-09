import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from milk.module.greeting import is_greeting, greeting
from milk.module.purchase import pay, get_total

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))


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
  if text.startswith("合計"):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=get_total(text.split())))
    return


if __name__ == "__main__":
  port = int(os.getenv("PORT", 8000))
  app.run(host="0.0.0.0", port=port)
