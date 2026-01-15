import os

CJPLUS_URL = os.getenv("CJPLUS_URL", "unknown")
CJPLUS_USERNAME = os.getenv("CJPLUS_USERNAME", "unknown")
CJPLUS_PASSWORD = os.getenv("CJPLUS_PASSWORD", "unknown")

EMAIL_SMTP_HOST = os.getenv("EMAIL_SMTP_HOST", "smtp.qq.com")
EMAIL_SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT", "465"))
EMAIL_SMTP_PASS = os.getenv("EMAIL_SMTP_PASS", "unknown")
EMAIL_SMTP_FROM = os.getenv("EMAIL_SMTP_FROM", "unknown")
EMAIL_SMTP_TO = os.getenv("EMAIL_SMTP_TO", "unknown")

SCREENSHOT_REPORTS = [
    # {
    #     "name": "今日新单报表",
    #     "page": 208,
    # },
    {
        "name": "延期出货明细表",
        "page": 220,
    },
    {
        "name": "宏智出货报表",
        "page": 210,
        "has_tail": False,
    },
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
