import logging
from croniter import croniter
from quantguard.config.account import Account, ExchangeName, MarketType
from quantguard.exchange.exchange import Exchange
from quantguard.config import settings
import time

logger = logging.getLogger(__name__)


class Worker:
    def __init__(self, account: Account, cron_config: str):
        self.name = account.name
        self.account: Account = account
        self.exchange: Exchange = self.create_exchange(account)
        # 定义 cron 表达式，例如 "10 * * * *" 表示每小时的第 10 分钟执行
        self.cron = croniter(cron_config, time.time())

    def create_exchange(self, account: Account) -> Exchange:
        config = {
            "apiKey": account.access_key,
            "secret": account.secret_key,
            "enableRateLimit": True,
        }
        # # 如果设置了代理，添加到配置中
        if settings.PROXY_URL:
            config["proxies"] = {
                "http": settings.PROXY_URL,
                "https": settings.PROXY_URL,
            }

        # 目前可能只有okx需要
        if account.passphrase:
            config["password"] = account.passphrase

        if account.exchange == ExchangeName.OKX.value:
            from quantguard.exchange.okx.ufutures import UFutures
            if account.market == MarketType.UFUTURES.value:
                return UFutures(account.name, config)

        elif account.exchange == ExchangeName.GATE.value:
            from quantguard.exchange.gate.ufutures import UFutures
            if account.market == MarketType.UFUTURES.value:
                return UFutures(account.name, config)
        raise Exception(f"account {account.name} exchange {account.exchange} market {account.market} not supported")

    async def run(self, func: callable):
        # while True:
        #     diff_time = self.cron.get_next() - time.time()
        #     await asyncio.sleep(diff_time)
        #     await func()
        await func()
