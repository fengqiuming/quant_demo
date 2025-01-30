from ib_insync import *

# 连接到交易服务器
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

# 获取所有持仓
positions = ib.positions()

# 遍历所有持仓并创建相应的清仓订单
for position in positions:
    contract = position.contract
    positionSize = position.position

    # 如果是多头持仓，创建市价卖出订单
    if positionSize > 0:
        order = MarketOrder('SELL', abs(positionSize))
        ib.placeOrder(contract, order)
    # 如果是空头持仓，创建市价买入订单
    elif positionSize < 0:
        order = MarketOrder('BUY', abs(positionSize))
        ib.placeOrder(contract, order)

# 断开链接
# ib.disconnect()