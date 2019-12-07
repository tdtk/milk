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

app = Flask(__name__)

line_bot_api = LineBotApi('nsXxbymNREOYtjASe9AT53KNmLCqlzU7EnmxaPAlRWCddRg0/xGltSVC73rDuJx5HxIRYvHxJXk7ezEYAHHz9AQ/hlofADQWz68tdFaRFcx0oeud082EyMH+3zIwn+IyTS9qASxbHJK3a8NgbrumlwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('77580d29d867a34863c8e83a9f625ac8')


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
  line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text=event.message.text))


if __name__ == "__main__":
  app.run()
