from ib_insync import IB, Stock, MarketOrder, LimitOrder

# Create IB instance and connect to TWS / IB Gateway
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)  # Default port is 7497, clientId is set as needed

# Define the stock
stock = Stock('TQQQ', 'SMART', 'USD')

# Qualify contracts (fetch information for the specified stock)
ib.qualifyContracts(stock)

# 1. Market order to buy 10 shares
market_order = MarketOrder('BUY', 10)
market_trade = ib.placeOrder(stock, market_order)
print(f'Market order placed: {market_trade}')

# 2. Limit order to buy 10 shares at $200
limit_order = LimitOrder('BUY', 10, 200)
limit_trade = ib.placeOrder(stock, limit_order)

print(f'Limit order placed: {limit_trade}')