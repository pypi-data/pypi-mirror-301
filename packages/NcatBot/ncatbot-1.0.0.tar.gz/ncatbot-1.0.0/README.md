# NcatBot SDK

NcatBot SDK 是一个用于创建和管理 QQ 机器人的 Python 库。它提供了一套完整的 API，用于处理 WebSocket 连接、发送和接收消息、处理请求和通知等。

## 安装

通过 pip 安装 NcatBot SDK：

```bash
pip install qqbot-sdk
```
## 快速开始
导入必要的模块：
```python
from NcatBot.ws import WebSocketClient
from NcatBot.hp import send_group_msg
from NcatBot.log import info
```
定义回调函数：
```python
def on_meta_event(msg):
    info(f"Meta event received: {msg}")

def on_message(msg):
    info(f"Message received: {msg}")
```
创建 WebSocket 客户端实例并运行：
```python
url = "ws://localhost:3001"
client = WebSocketClient(url, meta_event=on_meta_event, message=on_message)
client.run()
```
发送群组消息：
```python
send_group_msg(group_id=12345, message="Hello, QQ Group!")
```

## 许可证
NcatBot SDK 是在 MIT 许可证下发布的。更多信息请参阅 LICENSE 文件。