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

    @contextlib.contextmanager
    def transaction(
        self,
    ) -> Generator[pymysql.Connection[pymysql.cursors.DictCursor], None, None]:
        """获取事务连接的上下文管理器（自动提交关闭）"""
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
                autocommit=False,
            )
            logger.debug(
                f"已连接到数据库(事务模式): {self.database}@{self.host}:{self.port}"
            )
            yield conn
            conn.commit()
            logger.debug(f"事务已提交: {self.database}")
        except Exception as e:
            if conn:
                conn.rollback()
                logger.warning(f"事务已回滚: {self.database} - {e}")
            logger.error(f"事务执行失败: {e}")
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

    def execute_batch_update(self, sql: str, params_list: List[tuple]) -> int:
        """在事务中批量执行更新/插入/删除操作，返回总影响行数"""
        total_affected = 0
        with self.transaction() as conn:
            with conn.cursor() as cursor:
                for params in params_list:
                    affected_rows = cursor.execute(sql, params)
                    total_affected += affected_rows
        return total_affected


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
