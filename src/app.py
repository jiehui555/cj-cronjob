import argparse
import sys
from src.jobs.it_screenshot_job import run_it_screenshot_job
from src.jobs.scheduler import run_scheduler


def run(job_name: str = "it-screenshot") -> int:
    """运行指定任务"""
    jobs = {
        "it-screenshot": run_it_screenshot_job,
    }

    if job_name not in jobs:
        print(f"错误: 未知的任务 '{job_name}'")
        print(f"可用任务: {', '.join(jobs.keys())}")
        return 1

    return jobs[job_name]()


def run_schedule():
    """运行定时调度器"""
    jobs = [
        ("截图任务", "08:00", run_it_screenshot_job),
    ]
    run_scheduler(jobs, run_once_at_start=False)


def main():
    """主入口 - 支持命令行参数"""
    parser = argparse.ArgumentParser(
        description="自动报表截图工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
可用命令:
  --run [任务名]    立即运行指定任务 (例如: it-screenshot)
  --schedule        启动定时调度器 (每天 08:00 执行)

示例:
  python main.py --run it-screenshot
  python main.py --schedule
        """,
    )

    parser.add_argument("--run", type=str, help="任务名称 (例如: it-screenshot)")
    parser.add_argument("--schedule", action="store_true", help="启动定时调度器")

    args = parser.parse_args()

    # 如果没有参数，显示帮助
    if len(sys.argv) == 1:
        parser.print_help()
        return 0

    # 处理命令
    if args.run:
        result = run(args.run)
        return result

    if args.schedule:
        run_schedule()
        return 0

    print("请指定 --run 或 --schedule 参数")
    return 1


if __name__ == "__main__":
    sys.exit(main())
