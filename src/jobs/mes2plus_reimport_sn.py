import datetime
import re
from src.services.mes_service import get_mes_service
from src.services.plus_service import get_plus_service
from src.tools.clock import now
from src.tools.logger import get_logger

logger = get_logger(__name__)


def run_mes2plus_reimport_sn_job() -> int:
    """MES2Plus-重新导入序列号"""

    # 连接数据库
    mes_service = get_mes_service()
    plus_service = get_plus_service()
    logger.info(f"MES 数据库版本: {mes_service.version}")
    logger.info(f"PLUS 数据库版本: {plus_service.get_version}")

    # 获取近期更新的条码生成记录
    barcode_creation_records = (
        mes_service.get_recently_updated_barcode_creation_records(
            start_date=(now() - datetime.timedelta(days=2)),
            stop_date=(now() + datetime.timedelta(days=1)),
        )
    )
    logger.info(f"近期更新的条码生成记录: {len(barcode_creation_records)} 条")

    # 遍历近期更新的条码生成记录
    for record in barcode_creation_records:
        order_code = _extract_order_number(record["order_code"])
        logger.info(f"正在处理条码生成记录: {record['task_code']} - {order_code}")

        # 查询导入的条码列表
        mes_imported_barcodes = mes_service.get_imported_barcodes(record["bc_id"])
        mes_codes = [code["code"] for code in mes_imported_barcodes]
        logger.info(f"MES 导入的条码列表: {len(mes_codes)} 条")

        # 查询 PLUS 已导入的条码列表
        plus_imported_barcodes = plus_service.get_inv_imported_barcodes(order_code)
        plus_codes = [code["code"] for code in plus_imported_barcodes]
        logger.info(f"PLUS 已导入的条码列表: {len(plus_codes)} 条")

        # 检查数量是否一致，不一致则跳过
        if len(mes_codes) != len(plus_codes):
            logger.warning("两边的条码数量不一致，跳过不处理")
            continue

        # 检查两边的条码是否一致，一致则跳过
        if set(mes_codes) == set(plus_codes):
            logger.warning("两边的条码内容一致，跳过不处理")
            continue

        # 查询 PLUS 已入/出库的条码列表
        plus_incoming_barcodes = plus_service.get_inv_incoming_barcodes(order_code)
        plus_outgoing_barcodes = plus_service.get_inv_outgoing_barcodes(order_code)
        if plus_incoming_barcodes or plus_outgoing_barcodes:
            logger.warning("已存在已入/出库的条码，跳过不处理")
            continue

        # 删除 PLUS 已导入的条码
        delete_count = plus_service.delete_inv_imported_barcodes(order_code)
        logger.info(f"删除 PLUS 已导入的条码: {delete_count} 条")

        # 将 MES 导入的条码列表导入 PLUS
        insert_count = plus_service.insert_inv_imported_barcodes(
            order_code, record["inv_code"], mes_imported_barcodes
        )
        logger.info(f"将 MES 导入的条码列表导入 PLUS: {insert_count} 条")

    return 0


def _extract_order_number(order: str) -> str:
    """从输入字符串中提取正确的订单号"""

    # 第一优先级：匹配带有 -数字-数字 后缀的订单号，只取主体部分
    pattern_with_suffix = r"[A-Z]+[A-Z0-9-]*(?=-[0-9]-[0-9])"
    match = re.search(pattern_with_suffix, order)
    if match:
        return match.group(0)

    # 第二优先级：普通订单号（无特定后缀）
    pattern_normal = r"[A-Z]+[A-Z0-9-]*"
    match = re.search(pattern_normal, order)
    if match:
        return match.group(0)

    return order
