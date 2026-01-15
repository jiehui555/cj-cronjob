from src.tools.clock import now
from src.tools.db.mysql import get_plus_db
from src.tools.logger import get_logger

logger = get_logger(__name__)


class PlusService:
    """PLUS系统数据库服务类"""

    def __init__(self):
        self.db = get_plus_db()

    @property
    def get_version(self) -> str:
        return self.db.get_version()

    def get_inv_imported_barcodes(self, order_code: str) -> list[dict]:
        """获取仓库已导入的条码"""
        sql = """
        SELECT
            `SN码` AS `code`
        FROM
            `物料扫码-SN库`
        WHERE
            `销售订单` = %s;
        """
        return self.db.execute_query(sql, (order_code,))

    def get_inv_incoming_barcodes(self, order_code: str) -> list[dict]:
        """获取仓库已入库的条码"""
        sql = """
        SELECT
            `SN码` AS `code`
        FROM
            `物料扫码-库存`
        WHERE
            `销售订单` = %s;
        """
        return self.db.execute_query(sql, (order_code,))

    def get_inv_outgoing_barcodes(self, order_code: str) -> list[dict]:
        """获取仓库已出库的条码"""
        sql = """
        SELECT
            `SN码` AS `code`
        FROM
            `物料扫码-出库`
        WHERE
            `销售订单` = %s;
        """
        return self.db.execute_query(sql, (order_code,))

    def delete_inv_imported_barcodes(self, order_code: str) -> int:
        """删除仓库已导入的条码"""
        sql = """
        DELETE FROM
            `物料扫码-SN库`
        WHERE
            `销售订单` = %s;
        """
        return self.db.execute_update(sql, (order_code,))

    def insert_inv_imported_barcodes(
        self, order_code: str, inv_code: str, barcodes: list[dict]
    ) -> int:
        """插入仓库已导入的条码"""
        sql = """
        INSERT INTO `物料扫码-SN库` (`销售订单`, `物料编码`, `SN码`, `导入来源`, `录入人`, `录入时间`)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        datetime_now = now().strftime("%Y-%m-%d %H:%M:%S")
        params_list = [
            (
                order_code,
                inv_code,
                barcode["code"],
                "机器人",
                "机器人",
                datetime_now,
            )
            for barcode in barcodes
        ]
        return self.db.execute_batch_update(sql, params_list)


# 工厂函数
def get_plus_service() -> PlusService:
    """获取PLUS服务实例"""
    return PlusService()
