import logging
import os
from playwright import sync_api

from src import config, now


def run() -> int:
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
        img_paths = []
        for report in config.reports:
            url = f'{config.base_url}/utl/{report["page"]}/{report["page"]}.php'
            logging.info(f'开始处理报表：{report["name"]} - {url}')

            # 根据报表名称选择对应的处理方式
            if report["name"] == "今日新单报表":
                img_paths.append(handle_today_new_order_report(page, url))
            else:
                pass

        print(img_paths)
    return 1


def handle_today_new_order_report(page: sync_api.Page, url: str) -> str:
    """ 截取「今日新单报表」 """

    # 访问数据表格页
    page.goto(url, wait_until="networkidle", timeout=60_000)
    page.wait_for_selector("#table", state="visible", timeout=5_000)

    # 截取所需数据
    img_path = f"今日新单报表_{now().strftime('%Y-%m-%d')}.png"
    page.locator("#table").screenshot(path=img_path)

    return img_path
