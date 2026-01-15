from __future__ import annotations

import contextlib
from typing import Generator, Optional, List, Dict, Any

import pymysql

from src import config
from src.tools.logger import get_logger

logger = get_logger(__name__)


class MySQLConnection:
    """MySQL数据库连接管理器"""

    def __init__(
        self,
        host: str,
        port: int,
        user: str,
        password: str,
        database: str,
        charset: str = "utf8mb4",
    ):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset

    @contextlib.contextmanager
    def get_connection(
        self,
    ) -> Generator[pymysql.Connection[pymysql.cursors.DictCursor], None, None]:
        """获取数据库连接的上下文管理器"""
        conn = None
        try:
            conn = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                charset=self.charset,
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True,
            )
            logger.debug(f"已连接到数据库: {self.database}@{self.host}:{self.port}")
            yield conn
        except Exception as e:
            logger.error(f"数据库连接失败: {e}")
            raise
        finally:
            if conn:
                conn.close()
                logger.debug(f"已关闭数据库连接: {self.database}")

    def get_version(self) -> str:
        """获取数据库版本"""
        sql = "SELECT @@VERSION AS version;"
        result = self.execute_query(sql)
        if result:
            return result[0]["version"]
        return ""

    def execute_query(
        self, sql: str, params: Optional[tuple] = None
    ) -> List[Dict[str, Any]]:
        """执行查询并返回结果"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params or ())
                return list(cursor.fetchall())

    def execute_update(self, sql: str, params: Optional[tuple] = None) -> int:
        """执行更新/插入/删除操作，返回影响行数"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                affected_rows = cursor.execute(sql, params or ())
                return affected_rows


# PLUS数据库连接实例
def get_plus_db() -> MySQLConnection:
    """获取PLUS数据库连接"""
    return MySQLConnection(
        host=config.DB_PLUS_MYSQL_HOST,
        port=config.DB_PLUS_MYSQL_PORT,
        user=config.DB_PLUS_MYSQL_USER,
        password=config.DB_PLUS_MYSQL_PASS,
        database=config.DB_PLUS_MYSQL_NAME,
    )


# MES数据库连接实例
def get_mes_db() -> MySQLConnection:
    """获取MES数据库连接"""
    return MySQLConnection(
        host=config.DB_MES_MYSQL_HOST,
        port=config.DB_MES_MYSQL_PORT,
        user=config.DB_MES_MYSQL_USER,
        password=config.DB_MES_MYSQL_PASS,
        database=config.DB_MES_MYSQL_NAME,
    )
