from quantguard.dao.clickhouse import ClickHouseConnector
from clickhouse_driver.errors import Error as ClickhouseError
import logging
from dataclasses import dataclass, asdict
from quantguard.common.enum import DimensionEnum

loggger = logging.getLogger(__name__)

db = ClickHouseConnector()


@dataclass
class Order:
    name: str  # account_name
    exchange: str  # exchange_id
    market_type: str  # 交易市场类型
    base_asset: str  # 基础资产
    quote_asset: str  # 计价资产
    market_order_id: str  # 交易所订单ID
    custom_order_id: str  # 自定义订单ID
    ts: int  # 下单时间
    origin_price: float  # 下单价格
    origin_quantity: float  # 下单数量
    total_average_price: float  # 总成交均价
    total_filled_quantity: float  # 总成交数量
    operation: str  # 操作 买/卖
    order_side: str  # 订单方向
    order_time_in_force: str  # 订单有效期
    reduce_only: int  # 是否只减仓
    order_type: str  # 订单类型
    order_state: str  # 订单状态
    dimension: DimensionEnum  # 交易量维度
    commission: float  # 手续费
    contract_size: float  # 合约大小
    info: str  # 原始信息
    created_at: int  # 创建时间

    def to_dict(self):
        return asdict(self)

    @classmethod
    def __tablename__(self):
        return "order"


class OrderDao:

    @staticmethod
    def insert(order: Order) -> bool:
        query = f"""
            INSERT INTO {Order.__tablename__()}
            (name, exchange, market_type, base_asset, quote_asset, market_order_id, custom_order_id, ts, origin_price, origin_quantity, total_average_price, total_filled_quantity, order_side, operation, order_time_in_force, reduce_only, order_type, order_state, dimension, commission, contract_size, info, created_at)
            VALUES
            """
        params = build_inster_params(order)
        sql = f"{query} {params}"
        try:
            db.execute(sql)
            return True
        except ClickhouseError as e:
            logging.error(f"insert order sql: {sql}, error: {e}")
        except Exception as e:
            logging.error(f"insert order sql: {sql}, an unexpected error occurred: {e}")
        return False

    @staticmethod
    def get_by_market_order_id(market_order_id: str) -> Order:
        query = f"SELECT * FROM {Order.__tablename__()} WHERE market_order_id = '{market_order_id}'"
        result = db.execute(query)
        if result:
            return Order(*result[0])
        return None


def build_inster_params(order: Order) -> str:
    return (
        order.name,
        order.exchange,
        order.market_type,
        order.base_asset,
        order.quote_asset,
        order.market_order_id,
        order.custom_order_id,
        order.ts,
        order.origin_price,
        order.origin_quantity,
        order.total_average_price,
        order.total_filled_quantity,
        order.order_side,
        order.operation,
        order.order_time_in_force,
        order.reduce_only,
        order.order_type,
        order.order_state,
        order.dimension,
        order.commission if order.commission is not None else 0,
        order.contract_size,
        order.info,
        order.created_at,
    )
