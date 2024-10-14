from enum import Enum, auto
from decimal import Decimal
from datetime import datetime
from typing import Dict, List, Optional

class Mode(Enum):
    """
    运行模式
    """

    Backtest = auto()
    """
    回测
    """
    Sandbox = auto()
    """
    模拟
    """
    Real = auto()
    """
    实盘
    """

class Type(Enum):
    """
    交易类型
    """

    Limit = auto()
    """
    限价交易
    """
    Market = auto()
    """
    市价交易
    """

class Side(Enum):
    """
    交易方向
    """

    Long = auto()
    """
    做多
    """
    Short = auto()
    """
    做空
    """

class TimeFrame(Enum):
    """
    时间周期
    """

    Minute = auto()
    """
    1分钟
    """
    Minute3 = auto()
    """
    3分钟
    """
    Minute5 = auto()
    """
    5分钟
    """
    Minute15 = auto()
    """
    15分钟
    """
    Minute30 = auto()
    """
    30分钟
    """
    Hour = auto()
    """
    1小时
    """
    Hour2 = auto()
    """
    2小时
    """
    Hour4 = auto()
    """
    4小时
    """
    Hour6 = auto()
    """
    6小时
    """
    Hour8 = auto()
    """
    8小时
    """
    Hour12 = auto()
    """
    12小时
    """
    Day = auto()
    """
    1天
    """
    Day3 = auto()
    """
    3天
    """
    Week = auto()
    """
    1周
    """
    Month = auto()
    """
    1月
    """

class OrderStatus(Enum):
    """
    订单状态
    """

    Created = auto()
    """
    创建
    """
    Submited = auto()
    """
    已提交
    """
    Pending = auto()
    """
    挂单中
    """
    Partial = auto()
    """
    部分成交
    """
    Completed = auto()
    """
    完全成交
    """
    Rejected = auto()
    """
    被拒绝
    """
    Canceled = auto()
    """
    已取消
    """

class Candle:
    """
    K线
    """

    time: int
    """
    开盘时间
    """
    open: float
    """
    开盘价
    """
    high: float
    """
    最高价
    """
    low: float
    """
    最低价
    """
    close: float
    """
    收盘价
    """
    size: float
    """
    数量
    """
    amount: float
    """
    金额
    """
    taker_size: float
    """
    吃单数量
    """
    taker_amount: float
    """
    吃单金额
    """
    trades: int
    """
    成交笔数
    """

class Order:
    """
    订单
    """

    symbol: str
    """
    交易对
    """
    id: str
    """
    ID
    """
    type: Type
    """
    类型
    """
    side: Side
    """
    方向
    """
    reduce: bool
    """
    减仓
    """
    leverage: Decimal
    """
    杠杆倍数
    """
    size: Decimal
    """
    数量
    """
    price: Decimal
    """
    价格
    """
    time: datetime
    """
    下单时间
    """
    margin: Decimal
    """
    保证金
    """
    deal_size: Decimal
    """
    成交数量
    """
    deal_price: Decimal
    """
    成交均价
    """
    deal_fee: Decimal
    """
    成交手续费
    """
    status: OrderStatus
    """
    状态
    """

def debug(*args):
    """
    输出调试消息
    """

def info(*args):
    """
    输出信息消息
    """

def warn(*args):
    """
    输出警告消息
    """

def error(*args):
    """
    输出错误消息
    """

def print(*args):
    """
    输出消息
    """

def str_to_date(s: str) -> datetime:
    """
    字符串转日期 `UTC+0`
    ---
    - 格式1 : 2000
    - 格式2 : 200001
    - 格式3 : 20000102
    - 格式4 : 2000010203
    - 格式5 : 200001020304
    - 格式6 : 20000102030405
    ---
    其他格式均返回错误
    """

def ms_to_date(ts: int) -> datetime:
    """
    毫秒转日期 `UTC+0`
    """

def now_ms() -> int:
    """
    当前毫秒时间戳
    """

def rand_id() -> str:
    """
    随机32位ID
    """

def acc_cash() -> Decimal:
    """
    账户资金
    """

def acc_avail_cash() -> Decimal:
    """
    账户可用资金
    """

def acc_margin() -> Decimal:
    """
    账户占用保证金
    """

def acc_pnl() -> Decimal:
    """
    账户未实现盈亏
    """

def pos_long_size(symbol: str) -> Optional[Decimal]:
    """
    做多仓位数量
    """

def pos_long_avail_size(symbol: str) -> Optional[Decimal]:
    """
    做多仓位可用数量
    """

def pos_long_price(symbol: str) -> Optional[Decimal]:
    """
    做多仓位均价
    """

def pos_long_margin(symbol: str) -> Optional[Decimal]:
    """
    做多仓位占用保证金
    """

def pos_long_pnl(symbol: str) -> Optional[Decimal]:
    """
    做多仓位未实现盈亏
    """

def pos_short_size(symbol: str) -> Optional[Decimal]:
    """
    做空仓位数量
    """

def pos_short_avail_size(symbol: str) -> Optional[Decimal]:
    """
    做空仓位可用数量
    """

def pos_short_price(symbol: str) -> Optional[Decimal]:
    """
    做空仓位均价
    """

def pos_short_margin(symbol: str) -> Optional[Decimal]:
    """
    做空仓位占用保证金
    """

def pos_short_pnl(symbol: str) -> Optional[Decimal]:
    """
    做空仓位未实现盈亏
    """

def pair_leverage(symbol: str) -> Optional[Decimal]:
    """
    交易对杠杆倍数
    """

def pair_margin(symbol: str) -> Optional[Decimal]:
    """
    交易对保证金
    """

def pair_mark_price(symbol: str) -> Optional[Decimal]:
    """
    交易对标记价格
    """

def pair_candle(symbol: str, tf: TimeFrame) -> Optional[Candle]:
    """
    交易对K线
    """

def pair_order(symbol: str, id: str) -> Optional[Order]:
    """
    交易对订单
    """

def pair_open_orders(symbol: str) -> List[Order]:
    """
    交易对有效订单
    """

def pair_order_ids(symbol: str) -> List[str]:
    """
    交易对订单IDS
    """

def pair_symbols() -> List[str]:
    """
    所有交易对
    """

def buy_long_limit(symbol: str, size: Decimal, price: Decimal) -> Optional[str]:
    """
    买入限价做多
    """

def sell_long_limit(symbol: str, size: Decimal, price: Decimal) -> Optional[str]:
    """
    卖出限价做多
    """

def buy_long_market(symbol: str, size: Decimal) -> Optional[str]:
    """
    买入市价做多
    """

def sell_long_market(symbol: str, size: Decimal) -> Optional[str]:
    """
    卖出市价做多
    """

def buy_short_limit(symbol: str, size: Decimal, price: Decimal) -> Optional[str]:
    """
    买入限价做空
    """

def sell_short_limit(symbol: str, size: Decimal, price: Decimal) -> Optional[str]:
    """
    卖出限价做空
    """

def buy_short_market(symbol: str, size: Decimal) -> Optional[str]:
    """
    买入市价做空
    """

def sell_short_market(symbol: str, size: Decimal) -> Optional[str]:
    """
    卖出市价做空
    """

def close_order(symbol: str, id: str):
    """
    取消订单
    """

def close_all_order(symbol: str):
    """
    取消所有订单
    """

def set_leverage(symbol: str, leverage: Decimal):
    """
    调整杠杆倍数
    """

def set_benchmark(symbol: str):
    """
    设置基准
    """

def set_pair(
    symbol: str,
    taker_fee_rate: Optional[Decimal] = None,
    maker_fee_rate: Optional[Decimal] = None,
):
    """
    设置交易对
    """

def is_running() -> bool:
    """
    是否运行中
    """

def trade_time() -> datetime:
    """
    当前交易时间
    """

def benchmark() -> str:
    """
    基准交易对
    """

def run(mode: Mode, strategy: str, params: dict):
    """
    运行策略
    """
