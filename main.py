import os
import random

import requests
from bs4 import BeautifulSoup
from flask import Flask, abort, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (MessageEvent, SourceUser, TextMessage,
                            TextSendMessage, VideoMessage, VideoSendMessage)

app = Flask(__name__)

# 環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


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


# ランダム返信用のリスト
randomResList = []

# random.txtから名言を読み込む
with open('random.txt', 'r') as f:
    # 一列ごとに読み込む
    for line in f:
        # 改行文字の削除
        stripedLine = line.rstrip()
        randomResList.append(stripedLine)

# keyと一致する入力ならvalueを出力する用の辞書
resDictionary = {
    "死ぬこと以外は": "かすり傷",
    "読書という": "荒野",
    "たった一人の": "熱狂"
}


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
        # 特定の単語が入っていなければリストからランダムで返信する
        reply = random.choice(randomResList)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply))


if __name__ == "__main__":
    # app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
