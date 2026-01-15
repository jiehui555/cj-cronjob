from datetime import datetime
from zoneinfo import ZoneInfo


def now():
    """获取当前时间"""
    return datetime.now(ZoneInfo("Asia/Shanghai"))
