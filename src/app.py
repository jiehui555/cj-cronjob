import logging
import os
import zipfile
from playwright import sync_api

from src import config, now
from src.email import send_email
from src.screenshot import handle_today_new_order_report, handle_delay_shipment_report, handle_shipment_report


def run() -> int:
    img_paths = []
    with sync_api.sync_playwright() as pw:
        # 打开网页
        browser = pw.chromium.launch(headless=True)
        logging.info('已启动浏览器')

        viewport = sync_api.ViewportSize(width=1920, height=1080)
        context = browser.new_context(viewport=viewport)
        logging.info('已创建上下文')

        page = context.new_page()
        logging.info('已创建新页面')

        # 登录后台
        page.goto(config.base_url, wait_until="networkidle", timeout=30_000)
        page.wait_for_selector("input[name=\"user\"]", timeout=5_000)
        logging.info('已加载登录页面')

        page.fill("input[name=\"user\"]", config.bot_username)
        page.fill("input[name=\"pass\"]", config.bot_password)
        page.click("input[type=\"submit\"]")
        page.wait_for_load_state("networkidle", timeout=30_000)
        logging.info('已成功登录后台')

        # 处理报表截图
        for report in config.reports:
            url = f'{config.base_url}/utl/{report["page"]}/{report["page"]}.php'
            logging.info(f'开始处理报表：{report["name"]} - {url}')

            # 根据报表名称选择对应的处理方式
            if report["name"] == "今日新单报表":
                img_path = handle_today_new_order_report(page, url)
            elif report["name"] == "延期出货明细表":
                img_path = handle_delay_shipment_report(page, url)
            else:
                img_path = handle_shipment_report(
                    page, url, report["name"], report.get("has_tail", False))

            img_paths.append(img_path)
            logging.info(f'已完成截图：{img_path}')

    # 打包图片
    zip_path = f"每日截图-打包-{now().strftime('%Y-%m-%d')}.zip"
    with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
        for result_img_path in img_paths:
            if os.path.exists(result_img_path):  # 可选：检查文件是否存在
                filename = os.path.basename(result_img_path)  # 只取文件名
                zipf.write(result_img_path, arcname=filename)
            else:
                logging.warning(f"文件不存在，跳过 {result_img_path}")
    logging.info(f'已打包图片：{zip_path}')

    # 发送邮件
    send_email(zip_path, img_paths)
    logging.info('已发送邮件')

    return 1
