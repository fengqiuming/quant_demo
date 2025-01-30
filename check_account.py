from ib_insync import *

# Create IB instance and connect to TWS / IB Gateway
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

# Get positions
positions = ib.positions()

# Print position details
print("持仓信息：")
for position in positions:
    print(f"合约: {position.contract.symbol}, 数量: {position.position}, 平均成本: {position.avgCost:.2f}, 市值: {int(position.position * position.avgCost)}")

# Get account summary for cash balance
account_summary = ib.accountSummary()

cash_balance = next((item.value for item in account_summary if item.tag == 'CashBalance' and item.currency == 'USD'), None)
cash_balance = float(cash_balance)

if cash_balance is not None:
    print(f"现金余额: {int(cash_balance)} USD")
else:
    print("无法获取现金余额")

# 断开链接
# ib.disconnect()
