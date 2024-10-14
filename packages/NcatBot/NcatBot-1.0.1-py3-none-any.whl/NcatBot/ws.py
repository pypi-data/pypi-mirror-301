import websocket
import json
from .handle import *



class WebSocketClient:
    def __init__(self, url, meta_event=None,
                 message=None, message_sent=None,
                 request=None, notice=None):
        self.url = url
        self.on_meta_event_callback = meta_event
        self.on_message_callback = message
        self.on_message_sent_callback = message_sent
        self.on_request_callback = request
        self.on_notice_callback = notice

    # 接收数据
    def on_message(self, ws, message):
        # 将message转化为对象
        message = json.loads(message)
        self.handle_message(message)

    # 处理数据
    def handle_message(self, message):
        post_type = message['post_type']

        # 根据 post_type 和 intent 进行处理
        if post_type == "meta_event":
            if self.on_meta_event_callback:
                meta_event_handle(message, self.on_meta_event_callback)
            else:
                pass
        elif post_type == "message":
            if self.on_message_callback:
                message_handle(message, self.on_message_callback)
            else:
                pass
        elif post_type == "message_sent":
            if self.on_message_sent_callback:
                message_sent_handle(message, self.on_message_sent_callback)
            else:
                pass
        elif post_type == "request":
            if self.on_request_callback:
                request_handle(message, self.on_request_callback)
            else:
                pass
        elif post_type == "notice":
            if self.on_notice_callback:
                notice_handle(message, self.on_notice_callback)
            else:
                pass
        else:
            warning("不存在的事件")

    def run(self):
        ws = websocket.WebSocketApp(self.url, on_message=self.on_message)
        ws.run_forever()
