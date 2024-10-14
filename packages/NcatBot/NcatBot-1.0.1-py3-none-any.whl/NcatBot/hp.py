import requests
import os
from .log import *

class HttpRequest:
    def post(endurl, json):
        response = requests.post(f"http://localhost:3000/{endurl}", json=json)
        return response
    

def send_group_msg(group_id, message):
    json={
        "group_id": group_id,
        "message": [{"data": {"text": message}, "type": "text"}],
    }
    HttpRequest.post("send_group_msg", json)
    
def send_group_at_msg(group_id, message, user_id):
    json={
        "group_id": group_id,
        "message": [{"data": {"qq": user_id}, "type": "at"},
                    {"data": {"text": f' {message}'}, "type": "text"}],
    }
    HttpRequest.post("send_group_msg", json)

def send_group_reply_msg(group_id, message_id, user_id, message):
    json={
        "group_id": group_id,
        "message": [{'type': 'reply', 'data': {'id': message_id}}, 
                    {'type': 'at', 'data': {'qq': user_id}}, 
                    {'type': 'text', 'data': {'text': f' {message}'}}]
    }
    HttpRequest.post("send_group_msg", json)
    
def send_group_image(group_id, image_path):
    new_file = os.path.abspath(os.path.join(os.getcwd(), image_path)).replace('\\', '\\\\')
    json={
        "group_id": group_id,
        "message": [{"data": {"file": "file:///" + new_file}, "type": "image"}],
    }
    HttpRequest.post("send_group_msg", json)
    
def send_group_file(group_id, file_path):
    new_file = os.path.abspath(os.path.join(os.getcwd(), file_path)).replace('\\', '\\\\')
    json={
        "group_id": group_id,
        "message": [{"data": {"file": "file:///" + new_file}, "type": "file"}],
    }
    HttpRequest.post("send_group_msg", json)
    
def send_group_video(group_id, video_path):
    new_file = os.path.abspath(os.path.join(os.getcwd(), video_path)).replace('\\', '\\\\')
    json={
        "group_id": group_id,
        "message": [{"data": {"file": "file:///" + new_file}, "type": "video"}],
    }
    HttpRequest.post("send_group_msg", json)
    
def send_group_record(group_id, record_path):
    new_file = os.path.abspath(os.path.join(os.getcwd(), record_path)).replace('\\', '\\\\')
    json={
        "group_id": group_id,
        "message": [{"data": {"file": "file:///" + new_file}, "type": "record"}],
    }
    HttpRequest.post("send_group_msg", json)
    
def send_group_dice(group_id, type):
    json={
        "group_id": group_id,
        "message": [{"data": {"type": type}, "type": "dice"}],
    }
    HttpRequest.post("send_group_msg", json)
    
def send_group_rps(group_id, type):
    json={
        "group_id": group_id,
        "message": [{"data": {"type": type}, "type": "rps"}],
    }
    HttpRequest.post("send_group_msg", json)

def send_group_music(group_id,songid):
    json={
        "group_id": group_id,
        "message": [{"type": "music", "data": {"type": "qq", "id": songid}}],
    }
    HttpRequest.post("send_group_msg", json)
    
def send_private_msg(user_id, message):
    json={
        "user_id": user_id,
        "message": [{"data": {"text": message}, "type": "text"}],
    }
    HttpRequest.post("send_private_msg", json)
    
def send_private_at_msg(user_id, message, group_id):
    json={
        "user_id": user_id,
        "message": [{"data": {"qq": group_id}, "type": "at"},
                    {"data": {"text": f' {message}'}, "type": "text"}],
    }
    HttpRequest.post("send_private_msg", json)
    
def send_private_reply_msg(user_id, message_id, group_id, message):
    json={
        "user_id": user_id,
        "message": [{'type': 'reply', 'data': {'id': message_id}}, 
                    {'type': 'at', 'data': {'qq': group_id}}, 
                    {'type': 'text', 'data': {'text': f' {message}'}}]
    }
    HttpRequest.post("send_private_msg", json)
    
def send_private_image(user_id, image_path):
    new_file = os.path.abspath(os.path.join(os.getcwd(), image_path)).replace('\\', '\\\\')
    json={
        "user_id": user_id,
        "message": [{"data": {"file": "file:///" + new_file}, "type": "image"}],
    }
    HttpRequest.post("send_private_msg", json)
    
def send_private_file(user_id, file_path):
    new_file = os.path.abspath(os.path.join(os.getcwd(), file_path)).replace('\\', '\\\\')
    json={
        "user_id": user_id,
        "message": [{"data": {"file": "file:///" + new_file}, "type": "file"}],
    }
    HttpRequest.post("send_private_msg", json)
    
def send_private_video(user_id, video_path):
    new_file = os.path.abspath(os.path.join(os.getcwd(), video_path)).replace('\\', '\\\\')
    json={
        "user_id": user_id,
        "message": [{"data": {"file": "file:///" + new_file}, "type": "video"}],
    }
    HttpRequest.post("send_private_msg", json)
    
def send_private_record(user_id, record_path):
    new_file = os.path.abspath(os.path.join(os.getcwd(), record_path)).replace('\\', '\\\\')
    json={
        "user_id": user_id,
        "message": [{"data": {"file": "file:///" + new_file}, "type": "record"}],
    }
    HttpRequest.post("send_private_msg", json)
    
def send_private_dice(user_id, type):
    json={
        "user_id": user_id,
        "message": [{"data": {"type": type}, "type": "dice"}],
    }
    HttpRequest.post("send_private_msg", json)
    
def send_private_rps(user_id, type):
    json={
        "user_id": user_id,
        "message": [{"data": {"type": type}, "type": "rps"}],
    }
    HttpRequest.post("send_private_msg", json)
    
def send_private_music(user_id,songid):
    json={
        "user_id": user_id,
        "message": [{"type": "music", "data": {"type": "qq", "id": songid}}],
    }
    HttpRequest.post("send_private_msg", json)
    
def set_avatar(image_path):
    new_file = os.path.abspath(os.path.join(os.getcwd(), image_path)).replace('\\', '\\\\')
    json={
        "file": "file:///" + new_file,
    }
    HttpRequest.post("set_qq_avatar", json)
    
def get_group_system_msg(group_id):
    json={
        "group_id": group_id,
    }
    response = HttpRequest.post("get_group_system_msg", json)
    info(response.json(),"get_group_system_msg")
    return response.json()
def get_file(file_id):
    json={
        "file_id": file_id,
    }
    response = HttpRequest.post("get_file", json)
    info(response.json(),"get_file")
    return response.json()

def forward_friend_single_msg(user_id, message_id):
    json={
        "user_id": user_id,
        "message_id": message_id,
    }
    HttpRequest.post("forward_friend_single_msg", json)
    
def forward_group_single_msg(group_id, message_id):
    json={
        "group_id": group_id,
        "message_id": message_id,
    }
    HttpRequest.post("forward_group_single_msg", json)
    
def set_msg_emoji_like(message_id, emoji_id):
    json={
        "message_id": message_id,
        "emoji_id": emoji_id,
    }
    HttpRequest.post("set_msg_emoji_like", json)
    
def mark_group_msg_as_read(group_id):
    json={
        "group_id": group_id,
    }
    HttpRequest.post("mark_group_msg_as_read", json)
    
def mark_private_msg_as_read(user_id):
    json={
        "user_id": user_id,
    }
    HttpRequest.post("mark_private_msg_as_read", json)
    
def get_robot_uin_range():
    response = HttpRequest.post("get_robot_uin_range", {})
    info(response.json(),"get_robot_uin_range")
    return response.json()

def get_friends_with_category():
    response = HttpRequest.post("get_friends_with_category", {})
    info(response.json(),"get_friends_with_category")
    return response.json()

def set_online_status(status, ext_status=None, battery_status=None):
    json={
        "status": status,
        "ext_status": ext_status,
        "battery_status": battery_status,
        }
    HttpRequest.post("set_online_status", json)
    
def set_self_longnick(longNick):
    json={
        "longNick": longNick,
    }
    HttpRequest.post("set_self_longnick", json)
    
    
    
    
