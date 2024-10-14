import time
from .log import *
from .message import *
def meta_event_handle(msg, callback=None):
    if msg["meta_event_type"]=="lifecycle":
        if msg["sub_type"]=="connect":
            info(f"QQbot:{msg['self_id']} 于 {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(msg['time']))} - WebSocket connect success")
            if callback:
                callback(msg)
        else:
            error("websocket connect failure")
    elif msg["meta_event_type"]=="heartbeat":
        pass
    else:
        pass
            
def message_handle(msg, callback=None):
    if msg["message_type"]=="private":
        # 将其归为私聊消息处理
        info(f"received private.msg:{msg}")
        if callback:
            callback(msg)
    elif msg["message_type"]=="group":
        # 将其归为群消息处理
        info(f"received group.msg:{msg}")
        if callback:
            callback(msg)
    else:
        pass

def message_sent_handle(msg, callback=None):
    info("Message sent successfully")
    if callback:
        callback(msg)

def request_handle(msg, callback=None):
    if msg["request_type"]=="friend":
        info(f"send friend.request:{msg}")
        if callback:
            callback(msg)
    elif msg["request_type"]=="group":# 加群请求	✅	需要管理员权限
        info(f"send group.request:{msg}")
        if callback:
            callback(msg)
    else:
        pass

def notice_handle(msg, callback=None):
    if msg["notice_type"]=="friend_add":
        info(f"received friend.add:{msg}")
        if callback:
            callback(msg)
    elif msg["notice_type"]=="friend_recall":
        info(f"received friend.recall:{msg}")
        if callback:
            callback(msg)
    elif msg["notice_type"]=="group_admin":
        info(f"received group.admin:{msg}")
        if callback:
            callback(msg)
    elif msg["notice_type"]=="group_ban":
        info(f"received group.ban:{msg}")
        if callback:
            callback(msg)
    elif msg["notice_type"]=="group_card":
        info(f"received group.card:{msg}")
        if callback:
            callback(msg)
    elif msg["notice_type"]=="group_decrease":
        info(f"received group.decrease:{msg}")
        if callback:
            callback(msg)
    elif msg["notice_type"]=="group_increase":
        info(f"received group.increase:{msg}")
        if callback:
            callback(msg)
    elif msg["notice_type"]=="group_recall":
        info(f"received group.recall:{msg}")
        if callback:
            callback(msg)
    elif msg["notice_type"]=="group_upload":
        info(f"received group.upload:{msg}")
        if callback:
            callback(msg)
    elif msg["notice_type"]=="group_msg_emoji_like":# 不稳定
        info(f"received group.msg.emoji.like:{msg}")
        if callback:
            callback(msg)
    elif msg["notice_type"]=="essence":
        info(f"received essence:{msg}")
        if callback:
            callback(msg)
    elif msg["notice_type"]=="notify":
        info(f"received notify:{msg}")
        if callback:
            callback(msg)
    else:
        pass