import os

base_url = os.getenv("BASE_URL", "unknown")
bot_username = os.getenv("BOT_USERNAME", "unknown")
bot_password = os.getenv("BOT_PASSWORD", "unknown")

smtp_host = os.getenv("SMTP_HOST", "smtp.qq.com")
smtp_port = int(os.getenv("SMTP_PORT", "465"))
smtp_pass = os.getenv("SMTP_PASS", "unknown")
smtp_from = os.getenv("SMTP_FROM", "unknown")
smtp_to = os.getenv("SMTP_TO", "unknown")

reports = [
    # {
    #     "name": "今日新单报表",
    #     "page": 208,
    # },
    {
        "name": "延期出货明细表",
        "page": 220,
    },
    # {
    #     "name": "宏智出货报表",
    #     "page": 210,
    #     "has_tail": False,
    # },
    # {
    #     "name": "技果出货报表",
    #     "page": 207,
    #     "has_tail": False,
    # },
    # {
    #     "name": "迅成出货报表",
    #     "page": 206,
    #     "has_tail": False,
    # },
    # {
    #     "name": "金安出货报表",
    #     "page": 212,
    #     "has_tail": False,
    # },
    # {
    #     "name": "长嘉出货报表",
    #     "page": 205,
    #     "has_tail": True,
    # },
]
