from quantguard.dao.clickhouse import ClickHouseConnector
from clickhouse_driver.errors import Error as ClickhouseError
from dataclasses import dataclass, asdict
import logging

loggger = logging.getLogger(__name__)

db = ClickHouseConnector()


@dataclass
class Position:
    name: str  # 账户名
    exchange: str  # 交易所
    market_type: str  # 交易市场类型
    base_asset: str  # 基础资产
    quote_asset: str  # 计价资产
    ts: int  # 开仓时间
    dimension: str  # 仓位方向
    quantity: float  # 仓位数量
    average_price: float  # 开仓均价
    unrealized_pnl: float  # 未实现盈亏 TODO 不需要记录已实现盈亏？
    liquidation_price: float  # 爆仓价格
    contract_size: float  # 合约大小
    info: str
    created_at: int  # 创建时间

    def to_dict(self):
        return asdict(self)

    @classmethod
    def __tablename__(self):
        return "position"

    @classmethod
    def __snapshot_tablename__(self):
        return "position_snapshot"


class PositionDao:

    @staticmethod
    def insert(position: Position) -> bool:
        query = f"""
        INSERT INTO {Position.__tablename__()}
        (name, exchange, market_type, base_asset, quote_asset, ts, dimension, quantity, average_price, unrealized_pnl, liquidation_price, contract_size, info, created_at)
        VALUES
        """
        params = build_inster_params(position)
        sql = f"{query} {params}"
        try:
            db.execute(sql)
            return True
        except ClickhouseError as e:
            logging.error(f"insert position sql: {sql}, error: {e}")
        except Exception as e:
            logging.error(
                f"insert position sql: {sql}, an unexpected error occurred: {e}"
            )
        return False

    @staticmethod
    def get_by_name(name: str) -> Position:
        query = f"SELECT * FROM {Position.__tablename__()} FINAL WHERE name = '{name}'"
        result = db.execute(query)
        if result:
            return Position(*result[0])
        return None

    @staticmethod
    def get_by_exchange(exchange: str) -> list[Position]:
        query = f"SELECT * FROM {Position.__tablename__()} FINAL WHERE exchange = '{exchange}'"
        result = db.execute(query)
        if result:
            return [Position(*r) for r in result]
        return []

    @staticmethod
    def insert_snapshot(position: Position):
        query = f"""
        INSERT INTO {Position.__snapshot_tablename__()}
        (name, exchange, market_type, base_asset, quote_asset, ts, dimension, quantity, average_price, unrealized_pnl, liquidation_price, contract_size, info, created_at)
        VALUES
        """
        params = build_inster_params(position)
        sql = f"{query} {params}"
        try:
            db.execute(sql)
            return True
        except ClickhouseError as e:
            logging.error(f"create_snapshot position sql: {sql}, error: {e}")
        except Exception as e:
            logging.error(
                f"create_snapshot position sql: {sql}, an unexpected error occurred: {e}"
            )
        return False


def build_inster_params(position: Position):
    return (
        position.name,
        position.exchange,
        position.market_type,
        position.base_asset,
        position.quote_asset,
        position.ts,
        position.dimension,
        position.quantity,
        position.average_price,
        position.unrealized_pnl,
        position.liquidation_price,
        position.contract_size,
        position.info,
        position.created_at,
    )
