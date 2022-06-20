import os
import time
from datetime import datetime

from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.models import (
  MessageEvent, TextSendMessage
)
from linebot.exceptions import (
  InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

line_bot_api = LineBotApi(settings.LINE_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

@csrf_exempt
def callback(request=HttpRequest):
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.body.decode('utf-8')
    pid = str(os.getpid())
    try:
        events = parser.parse(body, signature)  # 傳入的事件
    except InvalidSignatureError:
        return HttpResponseForbidden()
    except LineBotApiError:
        return HttpResponseBadRequest()

    for event in events:
        if isinstance(event, MessageEvent):  # 如果有訊息事件
            line_bot_api.reply_message(  # 回復傳入的訊息文字
                event.reply_token,
                TextSendMessage(text='pid: ' + pid + ' - ' + event.message.text)
            )
    return HttpResponse()

@csrf_exempt
def test(request=HttpRequest):
    pid = str(os.getpid())
    # time.sleep(1)
    timeinmillionsec = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    return HttpResponse('datetime in million secs:' + timeinmillionsec + ' - request was processed by pid: '  + pid)