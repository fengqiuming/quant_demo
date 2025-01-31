import time
timestamp = time.time()

# import finnhub
# finnhub_client = finnhub.Client(api_key="cubg66hr01qsc2slmepgcubg66hr01qsc2slmeq0")
# print(finnhub_client.symbol_lookup('1860.HK'))
# print(finnhub_client.stock_candles('1860.HK', '1', 1590988249, 1591852249))
# print(finnhub_client.quote('AAPL'))

# import tushare as ts
# ts.set_token('c861d9f239ccbec622c1af88e36a9bec42cd69cdfb9db28f59dfb902')

# pro = ts.pro_api()
# df = pro.hk_basic()

# print(df)

from tradingview_ta import TA_Handler, Exchange, Interval, __version__
# print(__version__)

tsla = TA_Handler(
  symbol='TQQQ',
  screener='america',
  exchange='NASDAQ',
  interval=Interval.INTERVAL_15_MINUTES
)

summary = tsla.get_analysis().summary
indicators = tsla.get_analysis().indicators
# exchange = tsla.get_indicators().values
print(indicators)