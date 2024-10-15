import toml
import logging
from quantguard.common.enum import ExchangeName, MarketType
from quantguard.config import settings
from dataclasses import dataclass

logger = logging.getLogger(__name__)


# Define an Account class to store account information
@dataclass
class Account:
    def __init__(
        self,
        name: str,
        exchange: ExchangeName,
        market: MarketType,
        access_key: str,
        secret_key: str,
        passphrase: str = None,
    ):
        self.name = name
        self.exchange = exchange
        self.market = market
        self.access_key = access_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __str__(self):
        return (
            f"Account(name={self.name}, exchange={self.exchange}, market={self.market})"
        )


def init_account() -> list[Account]:
    # Read and parse the TOML file
    with open(settings.SYNC_OMEAGA.config_file, "r") as file:
        config = toml.load(file)

    tmp_accounts = {}
    # Extract accounts from the parsed TOML
    for account_data in config.get("accounts", []):
        for market in account_data["markets"]:
            account = Account(
                name=account_data["name"],
                exchange=ExchangeName(account_data["exchange"].lower()),
                market=market,
                access_key=account_data["access_key"],
                secret_key=account_data["secret_key"],
                passphrase=account_data.get("passphrase"),  # passphrase is optional
            )
            key = "%s:%s:%s" % (account.exchange.value, market, account_data["name"])
            tmp_accounts[key] = account

    sync_account: list = settings.SYNC_OMEAGA.account
    if not sync_account:
        raise ValueError("sync_account is not set in settings")

    accounts = []
    # 校验一下参数
    for account in sync_account:
        if tmp_accounts.get(account, None):
            accounts.append(tmp_accounts.get(account))
            logger.info(f"Add account: {account}")
    return accounts
