from datetime import datetime
import logging
import os
from zoneinfo import ZoneInfo

from dotenv import load_dotenv


def now():
    """ 获取当前时间 """
    return datetime.now(ZoneInfo("Asia/Shanghai"))


# 加载环境变量
load_dotenv()

# 配置日志格式
logging.Formatter.converter = lambda *args: now().timetuple()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# 清除 png 文件（残余图片）
for file in os.listdir():
    if file.lower().endswith(('.png', '.zip')):
        os.remove(file)

