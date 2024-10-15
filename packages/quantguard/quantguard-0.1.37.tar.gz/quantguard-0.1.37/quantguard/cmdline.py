import asyncio
import click
from logging.config import dictConfig

from quantguard.config import settings
from quantguard.config.account import init_account
from quantguard.worker.bill_worker import BillWorker

import logging

logger = logging.getLogger(__name__)


def init_log():
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "sample": {
                "format": "[%(asctime)s - %(name)s:%(lineno)d - %(levelname)s] %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "verbose": {
                "format": "[%(asctime)s - %(name)s:%(lineno)d - %(levelname)s] %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "formatter": "verbose",
                "level": "DEBUG",
                "class": "logging.StreamHandler",
            },
            "file": {
                "formatter": "verbose",
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "filename": settings.LOG_FILE,  # 指定日志文件的路径
                "mode": "a",  # 'a' 表示追加模式, 'w' 表示覆盖模式
                "encoding": "utf-8",
            },
        },
        "loggers": {
            "": {"level": settings.LOG_LEVEL, "handlers": settings.LOG_HANDLER},
        },
    }

    dictConfig(log_config)


@click.group(invoke_without_command=True)
@click.pass_context
@click.option("-V", "--version", is_flag=True, help="Show version and exit.")
def main(ctx, version):
    if version:
        click.echo(settings.VERSION)
    elif ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@main.command()
@click.option("--level", help="Log level")
@click.option("--work", help="bill, summary")
def server(level, work):
    _before_run()
    """Start server."""
    kwargs = {
        "LOGLEVEL": level,
    }
    print(f"work: {work}")
    print(kwargs)
    for name, value in kwargs.items():
        if value:
            settings.set(name, value)
    if work is None or work == "bill":
        run_bill_worker()


def _before_run():
    init_log()
    # set datadog ddtrace,
    # 将错误日志收集至 datadog, 步骤：
    # 1. 代码入口设置 ddtrace_config， 参考：https://gitlab.flyw.io/strategy/quantrade/-/blob/main/main.py?ref_type=heads#L41
    # 2. asyncio.create_task 收敛入口做ddtrace wrapper，如果不wrapper，不会被捕获。参考代码：https://gitlab.flyw.io/strategy/quantrade/-/blob/main/quantrade/misprice_funding_fee/common.py?ref_type=heads#L466
    # 3. 使用 ddtrace run 代替 python run, 参考：https://gitlab.flyw.io/strategy/quantrade/-/blob/main/Makefile?ref_type=heads#L23
    pass


def run_bill_worker():
    accounts = init_account()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)  # 设置当前事件循环

    tasks = []
    for account in accounts:
        task = loop.create_task(BillWorker(account=account).run())
        tasks.append(task)

    # 等待所有任务完成
    loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()
