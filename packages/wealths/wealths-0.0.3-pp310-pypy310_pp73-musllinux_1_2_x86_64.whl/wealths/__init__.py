from .wealths import *
from decimal import Decimal
from datetime import datetime
import polars as pl


BACKTEST = Mode.Backtest
"""
回测
"""
SANDBOX = Mode.Sandbox
"""
模拟
"""
REAL = Mode.Real
"""
实盘
"""

LIMIT = Type.Limit
"""
限价交易
"""
MARKET = Type.Market
"""
市价交易
"""

LONG = Side.Long
"""
做多
"""
SHORT = Side.Short
"""
做空
"""

TF_1M = TimeFrame.Minute
"""
1分钟
"""
TF_3M = TimeFrame.Minute3
"""
3分钟
"""
TF_5M = TimeFrame.Minute5
"""
5分钟
"""
TF_15M = TimeFrame.Minute15
"""
15分钟
"""
TF_30M = TimeFrame.Minute30
"""
30分钟
"""
TF_1H = TimeFrame.Hour
"""
1小时
"""
TF_2H = TimeFrame.Hour2
"""
2小时
"""
TF_4H = TimeFrame.Hour4
"""
4小时
"""
TF_6H = TimeFrame.Hour6
"""
6小时
"""
TF_8H = TimeFrame.Hour8
"""
8小时
"""
TF_12H = TimeFrame.Hour12
"""
12小时
"""
TF_1D = TimeFrame.Day
"""
1天
"""
TF_3D = TimeFrame.Day3
"""
3天
"""
TF_1W = TimeFrame.Week
"""
1周
"""
TF_1MO = TimeFrame.Month
"""
1月
"""

OS_CREATED = OrderStatus.Created
"""
创建
"""
OS_SUBMITED = OrderStatus.Submited
"""
已提交
"""
OS_PENDING = OrderStatus.Pending
"""
挂单中
"""
OS_PARTIAL = OrderStatus.Partial
"""
部分成交
"""
OS_COMPLETED = OrderStatus.Completed
"""
完全成交
"""
OS_REJECTED = OrderStatus.Rejected
"""
被拒绝
"""
OS_CANCELED = OrderStatus.Canceled
"""
已取消
"""


OS_REDUCE = True
"""
减仓
"""


S_BTC = "BTCUSDT"
S_ETH = "ETHUSDT"
S_SOL = "SOLUSDT"
S_BNB = "BNBUSDT"
S_APT = "APTUSDT"
S_SUI = "SUIUSDT"
S_ARB = "ARBUSDT"
S_OP = "OPUSDT"
S_LTC = "LTCUSDT"
S_TRX = "TRXUSDT"
S_ETC = "ETCUSDT"
S_UNI = "UNIUSDT"
S_1000PEPE = "1000PEPEUSDT"
S_XRP = "XRPUSDT"
S_DOGE = "DOGEUSDT"
S_NEIRO = "NEIROUSDT"
S_CAKE = "CAKEUSDT"
S_WIF = "WIFUSDT"
S_WLD = "WLDUSDT"
S_POPCAT = "POPCATUSDT"
S_1000SHIB = "1000SHIBUSDT"
S_TAO = "TAOUSDT"
S_ORDI = "ORDIUSDT"
S_REEF = "REEFUSDT"
S_SAGA = "SAGAUSDT"
S_ARK = "ARKUSDT"
S_TIA = "TIAUSDT"
S_SEI = "SEIUSDT"
S_NEIROETH = "NEIROETHUSDT"
S_1000BONK = "1000BONKUSDT"
S_1000SATS = "1000SATSUSDT"
S_EIGEN = "EIGENUSDT"
S_CATI = "CATIUSDT"
S_FTM = "FTMUSDT"
S_PEOPLE = "PEOPLEUSDT"
S_1MBABYDOGE = "1MBABYDOGEUSDT"
S_NOT = "NOTUSDT"
S_FET = "FETUSDT"
S_ENA = "ENAUSDT"
S_AVAX = "AVAXUSDT"
S_DOGS = "DOGSUSDT"
S_CELO = "CELOUSDT"
S_NEAR = "NEARUSDT"
S_1000FLOKI = "1000FLOKIUSDT"
S_TURBO = "TURBOUSDT"
S_HMSTR = "HMSTRUSDT"
S_DIA = "DIAUSDT"
S_MEW = "MEWUSDT"
S_ADA = "ADAUSDT"
S_AAVE = "AAVEUSDT"
S_1000RATS = "1000RATSUSDT"
S_BOME = "BOMEUSDT"
S_LINK = "LINKUSDT"
S_CFX = "CFXUSDT"
S_UXLINK = "UXLINKUSDT"
S_TON = "TONUSDT"
S_STX = "STXUSDT"
S_ORBS = "ORBSUSDT"
S_RENDER = "RENDERUSDT"
S_INJ = "INJUSDT"
S_FIL = "FILUSDT"
S_W = "WUSDT"
S_DOT = "DOTUSDT"
S_ONDO = "ONDOUSDT"
S_VIDT = "VIDTUSDT"
S_GALA = "GALAUSDT"
S_ARKM = "ARKMUSDT"
S_PHB = "PHBUSDT"
S_ETHFI = "ETHFIUSDT"
S_IO = "IOUSDT"
S_OM = "OMUSDT"
S_ZRO = "ZROUSDT"
S_BCH = "BCHUSDT"
S_DYDX = "DYDXUSDT"
S_ALT = "ALTUSDT"
S_MKR = "MKRUSDT"
S_BNX = "BNXUSDT"
S_AR = "ARUSDT"
S_CRV = "CRVUSDT"
S_TRB = "TRBUSDT"
S_ATOM = "ATOMUSDT"
S_RUNE = "RUNEUSDT"
S_BANANA = "BANANAUSDT"
S_BIGTIME = "BIGTIMEUSDT"
S_SUN = "SUNUSDT"
