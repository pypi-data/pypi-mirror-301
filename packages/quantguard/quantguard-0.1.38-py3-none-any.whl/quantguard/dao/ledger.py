from quantguard.dao.clickhouse import ClickHouseConnector
from clickhouse_driver.errors import Error as ClickhouseError
from dataclasses import dataclass, asdict
from quantguard.common.enum import LedgerType
import logging

loggger = logging.getLogger(__name__)

db = ClickHouseConnector()


@dataclass
class Ledger:
    name: str  # 账户名
    exchange: str  # 交易所
    asset: str  # 统计资产币种
    symbol: str  # 交易对
    ts: int  # 时间戳
    market_type: str  # 交易市场类型
    market_id: str  # 交易所ID
    trade_id: str  # 交易ID
    order_id: str  # 订单ID
    ledger_type: LedgerType  # 账目类型
    amount: float  # 金额
    info: str  # 原始信息
    created_at: int  # 创建时间

    def to_dict(self):
        return asdict(self)

    @classmethod
    def __tablename__(self):
        return "ledger"


class LedgerDao:

    @staticmethod
    def insert(ledger: Ledger) -> bool:

        query = f"""
            INSERT INTO {Ledger.__tablename__()}
            (name, exchange, asset, symbol, ts, market_type, market_id, trade_id, order_id, ledger_type, amount, info, created_at)
            VALUES
            """
        params = build_inster_params(ledger)
        sql = f"{query} {params}"
        try:
            db.execute(sql)
            return True
        except ClickhouseError as e:
            logging.error(f"insert ledger sql: {sql}, error: {e}")
        except Exception as e:
            logging.error(
                f"insert ledger sql: {sql}, an unexpected error occurred: {e}"
            )
        return False

    @staticmethod
    def get_by_market_id(market_id: str, ledger_type: str) -> Ledger:
        query = f"SELECT * FROM {Ledger.__tablename__()} WHERE market_id = '{market_id}' and ledger_type = '{ledger_type}'"
        result = db.execute(query)
        if result:
            return Ledger(*result[0])
        return None


def build_inster_params(ledger: Ledger) -> str:
    return (
        ledger.name,
        ledger.exchange,
        ledger.asset,
        ledger.symbol,
        ledger.ts,
        ledger.market_type,
        ledger.market_id,
        ledger.trade_id,
        ledger.order_id,
        ledger.ledger_type,
        ledger.amount,
        ledger.info,
        ledger.created_at,
    )
