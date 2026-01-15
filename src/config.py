import os

# PLUS 系统配置
CJPLUS_URL = os.getenv("CJPLUS_URL", "unknown")
CJPLUS_USERNAME = os.getenv("CJPLUS_USERNAME", "unknown")
CJPLUS_PASSWORD = os.getenv("CJPLUS_PASSWORD", "unknown")

# 邮件配置
EMAIL_SMTP_HOST = os.getenv("EMAIL_SMTP_HOST", "smtp.qq.com")
EMAIL_SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT", "465"))
EMAIL_SMTP_PASS = os.getenv("EMAIL_SMTP_PASS", "unknown")
EMAIL_SMTP_FROM = os.getenv("EMAIL_SMTP_FROM", "unknown")
EMAIL_SMTP_TO = os.getenv("EMAIL_SMTP_TO", "unknown")

# PLUS 系统数据库
DB_PLUS_MYSQL_HOST = os.getenv("DB_PLUS_MYSQL_HOST", "unknown")
DB_PLUS_MYSQL_PORT = int(os.getenv("DB_PLUS_MYSQL_PORT", "3306"))
DB_PLUS_MYSQL_USER = os.getenv("DB_PLUS_MYSQL_USER", "unknown")
DB_PLUS_MYSQL_PASS = os.getenv("DB_PLUS_MYSQL_PASS", "unknown")
DB_PLUS_MYSQL_NAME = os.getenv("DB_PLUS_MYSQL_NAME", "unknown")

# MES 系统数据库
DB_MES_MYSQL_HOST = os.getenv("DB_MES_MYSQL_HOST", "unknown")
DB_MES_MYSQL_PORT = int(os.getenv("DB_MES_MYSQL_PORT", "3306"))
DB_MES_MYSQL_USER = os.getenv("DB_MES_MYSQL_USER", "unknown")
DB_MES_MYSQL_PASS = os.getenv("DB_MES_MYSQL_PASS", "unknown")
DB_MES_MYSQL_NAME = os.getenv("DB_MES_MYSQL_NAME", "unknown")

# 需要截图的报表
SCREENSHOT_REPORTS = [
    {
        "name": "今日新单报表",
        "page": 208,
    },
    {
        "name": "延期出货明细表",
        "page": 220,
    },
    {
        "name": "宏智出货报表",
        "page": 210,
        "has_tail": False,
    },
    {
        "name": "技果出货报表",
        "page": 207,
        "has_tail": False,
    },
    {
        "name": "迅成出货报表",
        "page": 206,
        "has_tail": False,
    },
    {
        "name": "金安出货报表",
        "page": 212,
        "has_tail": False,
    },
    {
        "name": "长嘉出货报表",
        "page": 205,
        "has_tail": True,
    },
]
