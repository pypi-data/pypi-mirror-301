# 当前文件记录了dao相关的一些公共定义， 枚举值，数据类，等
from enum import Enum


# 枚举值
# ledger_type: "funding_fee|transfer_in|transfer_out|deposit|withdraw|deposit_sub|withdraw_sub"
class LedgerType(Enum):
    FUNDING_FEE = "funding_fee"
    TRADE_PNL = "trade_pnl"
    POSITION_CHANGE = "position_change"
    COMMISSION_FEE = "commission_fee"
    TRANSFER_IN = "transfer_in"
    TRANSFER_OUT = "transfer_out"
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    DEPOSIT_SUB = "deposit_sub"
    WITHDRAW_SUB = "withdraw_sub"


# 交易量维度
class DimensionEnum(Enum):
    LOT = "Lot"  # 张
    QUANTITY = "Quantity"  # 币


# 交易所名称
class ExchangeName(str, Enum):
    OKX = "okx"
    GATE = "gate"


# 交易市场类型
class MarketType(str, Enum):
    UFUTURES = "UFUTURES"
