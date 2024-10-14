import logging
from colorama import init, Fore, Style
import time

# 初始化colorama
init(autoreset=True)

# 创建一个logger
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)  # 设置日志级别

# 创建一个handler，用于将日志输出到控制台
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# 定义日志格式
class CustomFormatter(logging.Formatter):
    def format(self, record):
        # 格式化时间戳
        created_time = time.strftime('%Y\\%m\\%d %H:%M:%S', time.localtime(record.created))
        # 根据日志级别设置颜色
        if record.levelno == logging.INFO:
            color = Fore.GREEN
        elif record.levelno == logging.WARNING:
            color = Fore.YELLOW
        elif record.levelno == logging.ERROR:
            color = Fore.RED
        else:
            color = ''
        
        # 格式化日志头部
        tip = getattr(record, 'tip', None)  # 获取tip属性
        if tip:
            head = f'[{created_time} {record.levelname}]({tip})'
        else:
            head = f'[{created_time} {record.levelname}]'
        
        # 格式化日志信息
        return f'{color}{head}{Style.RESET_ALL}\n{record.msg}'

# 设置控制台handler的格式
console_handler.setFormatter(CustomFormatter())

# 添加handler到logger
logger.addHandler(console_handler)

def info(msg, tip=None):
    logger.info(msg, extra={'tip': tip})  # 传递tip参数

def warning(msg, tip=None):
    logger.warning(msg, extra={'tip': tip})  # 传递tip参数

def error(msg, tip=None):
    logger.error(msg, extra={'tip': tip})  # 传递tip参数
