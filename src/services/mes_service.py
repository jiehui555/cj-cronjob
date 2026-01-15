from datetime import datetime

from src.tools.db.mysql import get_mes_db
from src.tools.logger import get_logger

logger = get_logger(__name__)


class MesService:
    """MES系统数据库服务类"""

    def __init__(self):
        self.db = get_mes_db()

    @property
    def version(self) -> str:
        return self.db.get_version()

    def get_recently_updated_barcode_creation_records(
        self, start_date: datetime, stop_date: datetime
    ) -> list[dict]:
        """获取近期更新的条码生成记录"""
        sql = """
        SELECT
            t1.bc_id,
            t3.task_code,
            t1.inv_code,
            t1.inv_name,
            t3.order_code
        FROM
            `jgmes_barcode_create` AS t1
            LEFT JOIN `jgmes_modeling_inventory` AS t2 ON t2.inv_code = t1.inv_code
            LEFT JOIN `jgmes_pm_production_task` AS t3 ON t3.task_code = t1.bill_code
        WHERE
            t1.last_update_date BETWEEN %s AND %s
            AND t2.ic_id = 270
        ORDER BY
            t1.last_update_date DESC
        """
        return self.db.execute_query(
            sql, (start_date.strftime("%Y-%m-%d"), stop_date.strftime("%Y-%m-%d"))
        )

    def get_imported_barcodes(self, bc_id: str) -> list[dict]:
        """获取导入的条码列表"""
        sql = """
        SELECT
            bd_id,
            `code`
        FROM
            jgmes_barcode_data
        WHERE
            bc_id = %s
            AND delete_flag = 0        
        """
        return self.db.execute_query(sql, (bc_id,))


# 工厂函数
def get_mes_service() -> MesService:
    """获取MES服务实例"""
    return MesService()
