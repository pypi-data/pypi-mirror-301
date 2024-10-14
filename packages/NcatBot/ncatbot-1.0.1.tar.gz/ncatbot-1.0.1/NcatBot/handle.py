import time
from .log import *
from .message import *
def meta_event_handle(msg, callback=None):
    if msg["meta_event_type"]=="lifecycle":
        if msg["sub_type"]=="connect":
            info(f"QQbot:{msg['self_id']} 于 {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(msg['time']))} 连接成功!","WebSocket connect success")
            if callback:
                callback(EventMessage(msg))
        else:
            error("websocket connect failure")
    elif msg["meta_event_type"]=="heartbeat":
        pass
    else:
        pass
            
def message_handle(msg, callback=None):
    if msg["message_type"]=="private":
        # 将其归为私聊消息处理
        info(msg,"接收到私聊消息")
        if callback:
            callback(Message(msg))
    elif msg["message_type"]=="group":
        # 将其归为群消息处理
        info(msg,"接收到群消息")
        if callback:
            callback(Message(msg))
    else:
        pass

def message_sent_handle(msg, callback=None):
    info(msg,"消息发送成功")
    if callback:
        callback(msg)

def request_handle(msg, callback=None):
    if msg["request_type"]=="friend":
        info(msg,"发送加好友请求")
        if callback:
            callback(msg)
    elif msg["request_type"]=="group":# 加群请求	✅	需要管理员权限
        info(msg,"发送加群请求")
        if callback:
            callback(msg)
    else:
        pass

def notice_handle(msg, callback=None):
    if msg["notice_type"]=="friend_add":
        info(msg,"接收到加好友通知")
        if callback:
            callback(msg)
    elif msg["notice_type"]=="friend_recall":
        info(msg,"接收到私聊消息撤回")
        if callback:
            callback(msg)
    elif msg["notice_type"]=="group_admin":
        info(msg,"接收到群管理员变动通知")
        if callback:
            callback(msg)
    elif msg["notice_type"]=="group_ban":
        info(msg,"接收到群禁言通知")
        if callback:
            callback(msg)
    elif msg["notice_type"]=="group_card":
        info(msg,"接收到群名片更新通知")
        if callback:
            callback(msg)
    elif msg["notice_type"]=="group_decrease":
        info(msg,"接收到群成员减少通知")
        if callback:
            callback(msg)
    elif msg["notice_type"]=="group_increase":
        info(msg,"接收到群成员增加通知")
        if callback:
            callback(msg)
    elif msg["notice_type"]=="group_recall":
        info(msg,"接收到群消息撤回通知")
        if callback:
            callback(msg)
    elif msg["notice_type"]=="group_upload":
        info(msg,"接收到群文件上传通知")
        if callback:
            callback(msg)
    elif msg["notice_type"]=="group_msg_emoji_like":# 不稳定
        info(msg,"接收到群表情表态通知")
        if callback:
            callback(msg)
    elif msg["notice_type"]=="essence":
        info(msg,"接收到精华消息通知")
        if callback:
            callback(msg)
    elif msg["notice_type"]=="notify":
        info(msg,"接收到其余通知消息")
        if callback:
            callback(msg)
    else:
        pass