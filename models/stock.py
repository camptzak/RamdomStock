from dataclasses_json import config, dataclass_json
from dataclasses import dataclass


@dataclass_json
@dataclass
class Stock:
    symbol: str
    # these below should probably be optional or have a default of "Not found"
    oneYearTargetEst: float = config(field_name="1y Target Est")
    fiftyTwoWeekRange: str = config(field_name="52 Week Range")
    ask: float = config(field_name="Ask")
    avgVolume: int = config(field_name="Avg. Volume")
    beta: float = config(field_name="Beta (5Y Monthly)")
    bid: float = config(field_name="Bid")
    dayRange: str = config(field_name="Day's Range")
    eps: float = config(field_name="EPS (TTM)")
    earningsDate: str = config(field_name="Earnings Date")
    exDividendDate: str = config(field_name="Ex-Dividend Date")
    forwardDividendYield: float = config(field_name="Forward Dividend & Yield")
    marketCap: str = config(field_name="Market Cap")
    open: float = config(field_name="Open")
    peRatio: float = config(field_name="PE Ratio (TTM)")
    previousClose: float = config(field_name="Previous Close")
    quotePrice: float = config(field_name="Quote Price", decoder=lambda x: round(x, 4))
    volume: int = config(field_name="Volume")
