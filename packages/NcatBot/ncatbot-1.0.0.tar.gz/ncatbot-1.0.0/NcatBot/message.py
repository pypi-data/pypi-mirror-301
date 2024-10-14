class GroupMessage:
    def __init__(self, data):
        self.self_id= data['self_id']
        self.user_id= data['user_id']
        self.time= data['time']
        self.message_id= data['message_id']
        self.message_seq= data['message_seq']
        self.real_id= data['real_id']
        self.message_type= data['message_type']
        
        # 解析 sender 字典
        self.sender_id= data['sender']['user_id']
        self.sender_nickname = data['sender']['nickname']
        self.sender_card= data['sender']['card']
        self.sender_role= data['sender']['role']
        
        self.raw_message= data['raw_message']
        self.font= data['font']
        self.sub_type= data['sub_type']
        
        # 解析 message 列表
        self.messages= [msg['data']['text'] for msg in data['message']]
        self.message_format= data['message_format']
        self.post_type= data['post_type']
        # 如果需要 group_id，也可以添加
        self.group_id= data.get('group_id', None)
