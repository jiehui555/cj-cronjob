import logging
import time
import schedule
from typing import List, Callable, Tuple

from src import now


def execute_job(job_name: str, job_func: Callable[[], int]):
    """执行任务并记录日志"""
    current_time = now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"{'='*50}")
    logging.info(f"开始任务: {job_name} - {current_time}")
    logging.info(f"{'='*50}")

    try:
        result = job_func()
        if result == 0:
            logging.info(f"✅ 任务 '{job_name}' 执行成功")
        else:
            logging.error(f"❌ 任务 '{job_name}' 失败，退出码: {result}")
        return result
    except Exception as e:
        logging.error(f"❌ 任务 '{job_name}' 执行异常: {e}", exc_info=True)
        return 1


def run_scheduler(
    jobs: List[Tuple[str, str, Callable[[], int]]], run_once_at_start: bool = True
):
    """
    主调度器 - 支持多个任务

    Args:
        jobs: 任务列表，每个元素为 (任务名, 执行时间, 任务函数)
              执行时间格式: "HH:MM" (24小时制), None表示不调度
        run_once_at_start: 是否在启动时立即运行一次所有任务
    """
    logging.info("=" * 60)
    logging.info("每日任务调度器已启动")
    logging.info(f"当前时间: {now().strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info("=" * 60)

    # 注册任务
    for job_name, schedule_time, job_func in jobs:
        if schedule_time:
            schedule.every().day.at(schedule_time).do(
                lambda jn=job_name, jf=job_func: execute_job(jn, jf)
            )
            logging.info(f"📅 已安排: {job_name} 于 {schedule_time}")

    # 启动时立即运行一次
    if run_once_at_start:
        logging.info("\n启动时运行所有任务进行测试...")
        for job_name, _, job_func in jobs:
            execute_job(job_name, job_func)

    # 持续运行
    logging.info("调度器运行中，等待定时任务...")
    try:
        while True:
            try:
                schedule.run_pending()
            except Exception as e:
                logging.error(f"调度器执行任务时发生异常: {e}", exc_info=True)
            time.sleep(60)  # 每分钟检查一次
    except KeyboardInterrupt:
        logging.info("调度器已手动退出")
