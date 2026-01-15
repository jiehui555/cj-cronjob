import logging
import os
from datetime import datetime
from typing import Optional


def get_logger(
    name: str,
    log_dir: Optional[str] = None,
    log_file: Optional[str] = None,
    level: int = logging.INFO,
) -> logging.Logger:
    """
    获取配置好的logger实例

    Args:
        name: logger名称，通常使用 __name__
        log_dir: 日志目录，如果为None则使用 tmp/logs/{日期}
        log_file: 日志文件名，如果为None则使用 {name}.log
        level: 日志级别，默认为 logging.INFO

    Returns:
        配置好的logger实例
    """
    logger = logging.getLogger(name)

    # 避免重复添加handler
    if logger.handlers:
        return logger

    # 设置日志目录
    if log_dir is None:
        from src import now
        log_date = now().strftime("%Y-%m-%d")
        log_dir = f"tmp/logs/{log_date}"

    # 创建日志目录
    os.makedirs(log_dir, exist_ok=True)

    # 设置日志文件路径
    if log_file is None:
        # 使用模块名作为日志文件名
        module_name = name.split(".")[-1] if "." in name else name
        log_file = f"{module_name}.log"

    log_path = os.path.join(log_dir, log_file)

    # 创建文件处理器
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )

    # 添加处理器并设置级别
    logger.addHandler(file_handler)
    logger.setLevel(level)

    return logger
