import os
import smtplib
from email.header import make_header
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src import now, config


def send_email(zip_path: str, img_paths: list[str]) -> None:
    """ 发送邮件 """
    # 邮件对象
    message = MIMEMultipart()
    message['Subject'] = f"每日截图 - {now().strftime('%Y-%m-%d')}"
    message['From'] = config.smtp_from
    message['To'] = config.smtp_to

    html = f"""
        <p>附件是今天的所有报表截图打包（{now().strftime('%Y-%m-%d')}）</p>
        <p>如有问题请检查运行状态</p>
    """
    message.attach(MIMEText(html, 'html'))

    # 添加附件
    with open(zip_path, 'rb') as file:
        message.attach(MIMEApplication(file.read(), Name=os.path.basename(zip_path)))

    # 发送邮件
    with smtplib.SMTP_SSL(config.smtp_host, config.smtp_port) as server:
        server.login(config.smtp_from, config.smtp_pass)
        server.sendmail(config.smtp_from, config.smtp_to, message.as_string())
        server.quit()
