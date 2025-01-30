from flask import Flask, request
from ib_insync import IB, LimitOrder, Stock, MarketOrder

app = Flask(__name__)

# 连接 IB
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

@app.route('/trade', methods=['POST'])
def webhook():
    data = request.json
    print(f"Received webhook data: {data}")

    # 解析交易信号
    contract = Stock('TQQQ', 'SMART', 'USD')
    # order = MarketOrder('BUY', 10)
    order = LimitOrder('BUY', 10, 82.8)
    order.outsideRth = True

    # ✅ 使用 `placeOrder()` 直接下单
    trade = ib.placeOrder(contract, order)
    print(trade)
    # ✅ `ib.sleep(1)` 让 IB 有时间处理订单（避免异步问题）
    while trade.orderStatus.status not in ('Filled', 'Cancelled', 'PreSubmitted'):
        print(trade.orderStatus.status)
        ib.sleep(0.5)  # 每 0.5 秒检查一次订单状态

    return "Order placed successfully", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, threaded=False)  # 关闭多线程，避免 IB 线程冲突
