import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Optional


def send_email(
    smtp_host: str,
    smtp_port: int,
    smtp_from: str,
    smtp_pass: str,
    to: str,
    subject: str,
    body: str,
    attachments: Optional[List[str]] = None,
    is_html: bool = True,
) -> None:
    """
    Send email

    Args:
        smtp_host: SMTP server host
        smtp_port: SMTP server port
        smtp_from: Sender email address
        smtp_pass: Sender email password
        to: Recipient email address
        subject: Email subject
        body: Email body content
        attachments: List of file paths to attach
        is_html: Whether body is HTML
    """
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = smtp_from
    message['To'] = to

    message.attach(MIMEText(body, 'html' if is_html else 'plain'))

    if attachments:
        for attachment_path in attachments:
            if os.path.exists(attachment_path):
                with open(attachment_path, 'rb') as file:
                    filename = os.path.basename(attachment_path)
                    message.attach(MIMEApplication(file.read(), Name=filename))

    with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
        server.login(smtp_from, smtp_pass)
        server.sendmail(smtp_from, [to], message.as_string())
        server.quit()


def send_report_email(
    smtp_host: str,
    smtp_port: int,
    smtp_from: str,
    smtp_pass: str,
    to: str,
    zip_path: str,
    subject: Optional[str] = None,
    body: Optional[str] = None,
) -> None:
    """
    Send report email with zip attachment

    Args:
        smtp_host: SMTP server host
        smtp_port: SMTP server port
        smtp_from: Sender email address
        smtp_pass: Sender email password
        to: Recipient email address
        zip_path: Path to zip file
        subject: Email subject (auto-generated if None)
        body: Email body (auto-generated if None)
    """
    from datetime import datetime

    if subject is None:
        subject = f"每日截图 - {datetime.now().strftime('%Y-%m-%d')}"

    if body is None:
        body = f"""
        <p>附件是今天的所有报表截图打包（{datetime.now().strftime('%Y-%m-%d')}）</p>
        <p>如有问题请检查运行状态</p>
        """

    send_email(
        smtp_host=smtp_host,
        smtp_port=smtp_port,
        smtp_from=smtp_from,
        smtp_pass=smtp_pass,
        to=to,
        subject=subject,
        body=body,
        attachments=[zip_path] if zip_path else None,
        is_html=True,
    )