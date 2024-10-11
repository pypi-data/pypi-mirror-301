from enum import Enum

from . import platform_pb2 as pb


class SubscribeMethod(Enum):
    """可用的订阅方法"""

    PING = "ping"
    """心跳"""
    TICKER = "ticker"
    """行情"""
    KLINE = "kline"
    """K线"""
    ORDER = "order"
    """订单"""
    CONFIG = "config"
    """配置"""
    INSTRUMENT = "instrument"
    """合约"""


class InstrumentKind(Enum):
    """可用的标的类型"""

    FUTURE = "1"  # 期货
    """期货"""
    OPTION = "2"  # 期权
    """期权"""
    COMBINATION = "3"  # 组合
    """组合"""
    SPOT = "4"  # 即期(现货)
    """即期(现货)"""
    FUTURE_TO_SPOT = "5"  # 期转现
    """期转现"""
    SPOT_OPTION = "6"  # 现货期权
    """现货期权"""
    TAS = "7"  # TAS合约
    """TAS合约"""
    METAL_INDEX = "8"  # 金属指数
    """金属指数"""


class OrderState:
    """订单状态"""

    UNKNOWN = pb.Order.STATE_UNKNOWN

    CREATED = pb.Order.STATE_CREATED
    """创建: 服务端收到订单请求,并入库"""

    SUBMITTED = pb.Order.STATE_SUBMITTED
    """已提交: 已经提交给交易所,并收到交易所提交成功的回报"""

    PARTIAL_FILLED = pb.Order.STATE_PARTIAL_FILLED
    """部分成交"""

    FILLED = pb.Order.STATE_FILLED
    """全部成交"""

    CANCELED = pb.Order.STATE_CANCELED
    """已经撤单"""

    REJECTED = pb.Order.STATE_REJECTED
    """拒绝: 交易所拒绝订单,返回错误信息"""

    EXPIRED = pb.Order.STATE_EXPIRED
    """失效: 订单失效, 隔交易日订单或者其他原因导致订单失效"""


class PositionSide:
    """持仓方向"""

    NET = pb.Position.SIDE_NET
    """净持仓"""
    LONG = pb.Position.SIDE_LONG
    """多头"""
    SHORT = pb.Position.SIDE_SHORT
    """空头"""
