"""
Screenshot job - handles screenshot capture and report generation
"""
import logging
import os
import zipfile
from playwright import sync_api

from src import config, now
from src.utils.email import send_report_email
from src.utils.image import merge_images


def handle_today_new_order_report(page: sync_api.Page, url: str) -> str:
    """截取「今日新单报表」"""
    page.goto(url, wait_until="networkidle", timeout=60_000)
    page.wait_for_selector("#table", state="visible", timeout=5_000)
    logging.info('已加载数据表格页')

    img_path = f"今日新单报表_{now().strftime('%Y-%m-%d')}.png"
    page.locator("#table").screenshot(path=img_path)
    logging.info(f'已截取数据表格页：{img_path}')

    return img_path


def handle_delay_shipment_report(page: sync_api.Page, url: str) -> str:
    """截取「延期出货明细表」"""
    page.goto(url, wait_until="networkidle", timeout=30_000)
    page.wait_for_selector("#table", state="visible", timeout=5_000)
    logging.info('已加载数据表格页')

    page.locator("#header").evaluate("el => el.style.display = 'none'")
    logging.info('已隐藏顶部表单')

    img_path = f"延期出货明细表_{now().strftime('%Y-%m-%d')}.png"
    page.locator("#table").screenshot(path=img_path)
    logging.info(f'已截取数据表格页：{img_path}')

    return img_path


def append_blank_month_tbody(locator: sync_api.Locator, thead_month: str | int):
    """添加空白的月份数据"""
    tbody = f"""
            <tbody data-type="{thead_month} 月">
                <tr class="bg-blue">
                    <th rowspan="5" class="border-left">{thead_month} 月</th>
                    <th>事业部</th>
                    <th class="border-right">订单</th>
                    <th>预出数</th>
                    <th>预收入（万）</th>
                    <th class="border-right text-red">预利润（万）</th>
                    <th>已出数</th>
                    <th>实收金额（万）</th>
                    <th class="border-right text-red">实收利润（万）</th>
                </tr>
                <tr><td class="bg-blue">TV</td><td class="border-right">-</td><td>-</td><td>-</td><td class="border-right text-red">-</td><td>-</td><td>-</td><td class="border-right text-red">-</td></tr>
                <tr><td class="bg-blue">SX</td><td class="border-right">-</td><td>-</td><td>-</td><td class="border-right text-red">-</td><td>-</td><td>-</td><td class="border-right text-red">-</td></tr>
                <tr><td class="bg-blue">MT</td><td class="border-right">-</td><td>-</td><td>-</td><td class="border-right text-red">-</td><td>-</td><td>-</td><td class="border-right text-red">-</td></tr>
                <tr><td class="bg-blue">小结</td><td class="border-right">-</td><td>-</td><td>-</td><td class="border-right text-red">-</td><td>-</td><td>-</td><td class="border-right text-red">-</td></tr>
            </tbody>
        """

    locator.evaluate("""
            (element, html) => {
                element.insertAdjacentHTML('beforeend', html);
            }
        """, arg=tbody)


def handle_shipment_report(page: sync_api.Page, url: str, report: str, has_tail: bool) -> str:
    """截取「出货报表」"""
    page.goto(url, wait_until="networkidle", timeout=30_000)
    page.wait_for_selector("table", state="visible", timeout=5_000)
    logging.info('已加载数据表格页')

    # 截取局部截图
    img_paths = []

    # 表头
    img_path = f"{report}_局部截图-表头.png"
    page.locator("thead").screenshot(path=img_path)
    img_paths.append(img_path)
    logging.info(f'已截取表头：{img_path}')

    # 延期出货
    img_path = f"{report}_局部截图-延期出货.png"
    page.locator('tbody[data-type="延期出货"]').screenshot(path=img_path)
    img_paths.append(img_path)
    logging.info(f'已截取延期出货：{img_path}')

    # 货尾
    if has_tail:
        img_path = f"{report}_局部截图-货尾.png"
        page.locator('tbody[data-type="货尾"]').screenshot(path=img_path)
        img_paths.append(img_path)
        logging.info(f'已截取货尾：{img_path}')

    # 月份数据
    for i in range(now().month, min(now().month + 3, 13)):
        css_locator = f'tbody[data-type="{i} 月"]'
        if page.locator(css_locator).count() == 0:
            append_blank_month_tbody(page.locator("table"), i)
            logging.info(f"添加空白的 {i} 月数据")
        img_path = f"{report}_局部截图-{i} 月.png"
        page.locator(css_locator).screenshot(path=img_path)
        img_paths.append(img_path)
        logging.info(f'已截取 {i} 月数据：{img_path}')

    # 处理跨年数据
    if now().month > 10:
        logging.info(f"当前月份 {now().month} > 10，需截取 {now().year + 1} 年 1、2 月数据")
        page.click("input[name=\"年份\"]", timeout=10_000)
        page.click(f"li[lay-ym=\"{now().year + 1}\"]", timeout=10_000)
        page.wait_for_load_state("networkidle", timeout=30_000)
        page.wait_for_selector("table", state="visible", timeout=10_000)

        for i in range(1, 3):
            css_locator = f'tbody[data-type="{i} 月"]'
            if page.locator(css_locator).count() == 0:
                append_blank_month_tbody(page.locator("table"), i)
                logging.info(f"添加空白的 {i} 月数据")
            img_path = f"{report}_局部截图-{i} 月.png"
            page.locator(css_locator).screenshot(path=img_path)
            img_paths.append(img_path)

    # 确定合并顺序
    if now().month < 11:
        months = range(now().month + 2, now().month - 1, -1)
    elif now().month == 11:
        months = [1, 12, 11]
    else:
        months = [2, 1, 12]

    merge_order = [f"{report}_局部截图-表头.png", f"{report}_局部截图-延期出货.png"]
    if has_tail:
        merge_order.append(f"{report}_局部截图-货尾.png")
    merge_order += [f"{report}_局部截图-{m} 月.png" for m in months]

    logging.info(f"需要合并的图片：{merge_order}")

    # 合并图片
    save_name = f"{report}_{now().strftime('%Y-%m-%d')}"
    full_img_path = merge_images(merge_order, save_name)
    logging.info(f"图片合并完成，保存路径: {full_img_path}")

    # 删除局部截图
    for img_path in merge_order:
        if os.path.exists(img_path):
            os.remove(img_path)

    return full_img_path


def run_screenshot_job() -> int:
    """执行完整的截图任务"""
    img_paths = []

    with sync_api.sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        logging.info('已启动浏览器')

        viewport = sync_api.ViewportSize(width=1920, height=1080)
        context = browser.new_context(viewport=viewport)
        logging.info('已创建上下文')

        page = context.new_page()
        logging.info('已创建新页面')

        # 登录
        page.goto(config.base_url, wait_until="networkidle", timeout=30_000)
        page.wait_for_selector("input[name=\"user\"]", timeout=5_000)
        logging.info('已加载登录页面')

        page.fill("input[name=\"user\"]", config.bot_username)
        page.fill("input[name=\"pass\"]", config.bot_password)
        page.click("input[type=\"submit\"]")
        page.wait_for_load_state("networkidle", timeout=30_000)
        logging.info('已成功登录后台')

        # 处理每个报表
        for report in config.reports:
            url = f'{config.base_url}/utl/{report["page"]}/{report["page"]}.php'
            logging.info(f'开始处理报表：{report["name"]} - {url}')

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
            if os.path.exists(result_img_path):
                filename = os.path.basename(result_img_path)
                zipf.write(result_img_path, arcname=filename)
            else:
                logging.warning(f"文件不存在，跳过 {result_img_path}")
    logging.info(f'已打包图片：{zip_path}')

    # 发送邮件
    send_report_email(
        smtp_host=config.smtp_host,
        smtp_port=config.smtp_port,
        smtp_from=config.smtp_from,
        smtp_pass=config.smtp_pass,
        to=config.smtp_to,
        zip_path=zip_path,
    )
    logging.info('已发送邮件')

    return 0