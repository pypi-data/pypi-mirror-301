class EventMessage:
    def __init__(self, data):
        self.time = data['time']
        self.self_id = data['self_id']
        self.post_type = data['post_type']
        self.meta_event_type = data['meta_event_type']
        self.sub_type = data['sub_type']
        
class Sender:
    def __init__(self, data: dict):
        self.user_id = data.get('user_id')
        self.nickname = data.get('nickname')
        self.card = data.get('card', '')


        

class Message:
    def __init__(self, data: dict):
        # 初始化属性
        self.time = data.get('time')
        self.self_id = data.get('self_id')
        self.user_id = data.get('user_id')
        self.message_id = data.get('message_id')
        self.message_seq = data.get('message_seq')
        self.real_id = data.get('real_id')
        self.message_type = data.get('message_type')
        self.sender = Sender(data.get('sender', {}))  # 将 sender 转换为 Sender 类的实例
        self.raw_message = data.get('raw_message')
        self.font = data.get('font')
        self.sub_type = data.get('sub_type')
        self.message: dict = data.get('message')
        self.post_type = data.get('post_type')
        self.group_id = data.get('group_id')
