import logging

from dotenv import load_dotenv

from src.tools.clock import now


# 加载环境变量
load_dotenv()

# 配置日志格式
logging.Formatter.converter = lambda *args: now().timetuple()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
