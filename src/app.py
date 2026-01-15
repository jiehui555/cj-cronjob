import argparse
import sys
from src.jobs.it_screenshot_job import run_it_screenshot_job
# from src.jobs.mes2plus_reimport_sn import run_mes2plus_reimport_sn_job
from src.jobs.scheduler import run_scheduler


def get_jobs_info():
    """获取所有任务的信息"""
    return [
        {
            "name": "it-screenshot",
            "description": "IT-截图任务",
            "schedule": "08:30",
            "function": run_it_screenshot_job,
        },
        # todo 暂时不启用
        # {
        #     "name": "mes2plus-reimport-sn",
        #     "description": "MES2Plus-重新导入序列号",
        #     "schedule": "10:00",
        #     "function": run_mes2plus_reimport_sn_job,
        # },
    ]


def run(job_name: str) -> int:
    """运行指定任务"""
    jobs_info = get_jobs_info()
    jobs_map = {job["name"]: job["function"] for job in jobs_info}

    if job_name not in jobs_map:
        print(f"错误: 未知的任务 '{job_name}'")
        print(f"可用任务: {', '.join(jobs_map.keys())}")
        return 1

    return jobs_map[job_name]()


def list_jobs():
    """列出所有可用任务"""
    jobs = get_jobs_info()
    print("\n📋 可用任务列表:")
    print("=" * 80)
    for job in jobs:
        print(f"任务名称: {job['name']}")
        print(f"描述:     {job['description']}")
        print(f"调度时间: {job['schedule']}")
        print("-" * 80)
    print(f"\n总计: {len(jobs)} 个任务")
    print("\n使用方法:")
    print("  python main.py --run <任务名称>     # 立即运行指定任务")
    return 0


def run_schedule():
    """运行定时调度器"""
    jobs_info = get_jobs_info()
    jobs = [(job["description"], job["schedule"], job["function"]) for job in jobs_info]
    run_scheduler(jobs, run_once_at_start=False)


def main():
    """主入口 - 支持命令行参数"""
    parser = argparse.ArgumentParser(
        description="长嘉自动化工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
可用命令:
  --list            列出所有可用任务
  --run [任务名]    立即运行指定任务 (例如: it-screenshot)
  --schedule        启动定时调度器 (每天 08:00 执行)

示例:
  python main.py --list
  python main.py --run it-screenshot
  python main.py --schedule
        """,
    )

    parser.add_argument("--list", action="store_true", help="列出所有可用任务")
    parser.add_argument("--run", type=str, help="任务名称 (例如: it-screenshot)")
    parser.add_argument("--schedule", action="store_true", help="启动定时调度器")

    args = parser.parse_args()

    # 如果没有参数，显示帮助
    if len(sys.argv) == 1:
        parser.print_help()
        return 0

    # 处理命令
    if args.list:
        return list_jobs()

    if args.run:
        result = run(args.run)
        return result

    if args.schedule:
        run_schedule()
        return 0

    print("请指定 --list, --run 或 --schedule 参数")
    return 1


if __name__ == "__main__":
    sys.exit(main())
