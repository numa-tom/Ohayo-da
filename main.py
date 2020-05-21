from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)

from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import (
    FollowEvent, MessageEvent, TextMessage, TextSendMessage, ImageMessage,ImageSendMessage, 
    TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction
)

import os
import pya3rt
import requests
import random
#import scrape as sc
#import urllib3.request

hello = ["おはよう", "おはよ", "おは", "おはよん", "おはよー", "おはようー", "おはようございます", "おはです", "おっはー", "おはヨーダ", "おきた", "ぽきた"]
bye = ["おやすみ", "おやすみなさい", "じゃ", "じゃあね", "バイバイ", "ばいばい", "しーゆー"]
app = Flask(__name__)

#環境変数取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]


line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# MessageEvent
'''
    if "天気" in push_text:
        line_bot_api.reply_message(
            event.reply_token,
            [
            TextSendMessage(text='位置情報を教えてください。'),
            TextSendMessage(text='line://nv/location')
            ]
        )

    ###else:
'''
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    push_text = event.message.text
    reply_text = talkapi_response(push_text)
    prob = random.random()
    if push_text in hello:
        reply_text = "おはヨーダ"
    elif push_text == "おみくじ":
        reply_text = lotte() + "なのダ"
    elif prob <= 0.05:
        reply_text = "わたしはおはヨーダ"
    elif prob <=0.2:
        reply_text = "「" + push_text + "」とはなんダ？"
    if push_text in bye:
        reply_text = "おやすミーダ"
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
'''
@handler.add(MessageEvent, message=LocationMessage)
def handle_location(event):
    text = event.message.address

    result = sc.get_weather_from_location(text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=result)
    )
'''
def talkapi_response(text):
    apikey = "DZZ7ZhFZ1vne4KAeJIN85Oiro3fzIbc5"
    client = pya3rt.TalkClient(apikey)
    response = client.talk(text)
    return ((response['results'])[0])['reply']

def lotte():
#奇跡0.0001、最強0.0005、大吉0.05、中吉0.1、小吉0.15、吉0.24、半吉0.05、末吉0.1939、小末吉0.03、凶0.1、小凶0.025、半凶0.005、末凶0.005、大凶0.05、最恐0.0005
    lot_prob = random.random()
    text = ""
    if lot_prob <= 0.0001:
        text = "奇跡"
    elif lot_prob <= 0.0006:
        text = "最強"
    elif lot_prob <= 0.0506:
        text = "大吉"
    elif lot_prob <= 0.1506:
        text = "中吉"
    elif lot_prob <= 0.3006:
        text = "小吉"
    elif lot_prob <= 0.5406:
        text = "吉"
    elif lot_prob <= 0.5906:
        text = "半吉"
    elif lot_prob <= 0.7845:
        text = "末吉"
    elif lot_prob <= 0.8145:
        text = "小末吉"
    elif lot_prob <= 0.9145:
        text = "凶"
    elif lot_prob <= 0.9395:
        text = "小凶"
    elif lot_prob <= 0.9445:
        text = "半凶"
    elif lot_prob <= 0.9495:
        text = "末凶"
    elif lot_prob <= 0.9995:
        text = "大凶"
    else:
        text = "最恐"
    return text

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)