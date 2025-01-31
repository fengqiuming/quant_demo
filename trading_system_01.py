from tradingview_ta import TA_Handler
from ib_insync import *
import pandas as pd
import time
from datetime import datetime
import signal
import sys

class TradingSystem:
    def __init__(self, symbol, exchange="NASDAQ", screener="america", interval="1h"):
        """
        初始化交易系统
        :param symbol: 交易品种代码
        :param exchange: 交易所
        :param screener: 市场区域
        :param interval: 时间周期
        """
        # TradingView设置
        self.handler = TA_Handler(
            symbol=symbol,
            exchange=exchange,
            screener=screener,
            interval=interval
        )
        
        # IB连接设置
        self.ib = IB()
        try:
            self.ib.connect('127.0.0.1', 7497, clientId=1)
        except Exception as e:
            print(f"无法连接到TWS: {e}")
            
        # 交易品种设置
        # self.contract = Stock(symbol, exchange, 'USD')
        self.contract = Stock(symbol, 'SMART', 'USD')
        
        # 交易状态
        self.position = 0
        self.last_signal = None
        
        # 程序控制
        self.is_running = True
        
        # 设置信号处理
        signal.signal(signal.SIGINT, self.handle_exit)
        signal.signal(signal.SIGTERM, self.handle_exit)
        print("按 Ctrl+C 终止程序")
    
    def handle_exit(self, signum, frame):
        """处理退出事件"""
        print("\n正在安全退出程序...")
        self.is_running = False
        
        # 如果有持仓，平掉所有仓位
        if self.position != 0:
            try:
                order = MarketOrder('SELL' if self.position > 0 else 'BUY', 
                                  abs(self.position))
                self.ib.placeOrder(self.contract, order)
                print("已平掉所有持仓")
            except Exception as e:
                print(f"平仓失败: {e}")
        
        # 断开连接
        if self.ib.isConnected():
            self.ib.disconnect()
        
        print("程序已安全退出")
        sys.exit(0)
    
    def get_indicators(self):
        """获取TradingView的技术分析指标"""
        try:
            analysis = self.handler.get_analysis()
            return {
                'MACD': analysis.indicators['MACD.macd'],
                'MACD_Signal': analysis.indicators['MACD.signal'],
                'RSI': analysis.indicators['RSI'],
                'MA20': analysis.indicators['SMA20'],
                'MA50': analysis.indicators['SMA50']
            }
        except Exception as e:
            print(f"获取指标失败: {e}")
            return None
    
    def analyze_market(self, indicators):
        """
        根据技术指标分析市场走势
        返回: 1 (买入信号), -1 (卖出信号), 0 (持仓不变)
        """
        if not indicators:
            return 0
            
        # MACD交叉策略
        macd_cross_up = (indicators['MACD'] > indicators['MACD_Signal'])
        macd_cross_down = (indicators['MACD'] < indicators['MACD_Signal'])
        print(f"the market's macd_cross_up is {macd_cross_up}")
        print(f"the market's macd_cross_down is {macd_cross_down}")
        
        # RSI超买超卖
        rsi_oversold = indicators['RSI'] < 30
        rsi_overbought = indicators['RSI'] > 70

        print(f"the RSI oversold is {rsi_oversold}")
        print(f"the RSI overbought is {rsi_overbought}")
        
        # MA趋势
        trend_up = indicators['MA20'] > indicators['MA50']
        trend_down = indicators['MA20'] < indicators['MA50']
        print(f"the trend up is {trend_up}")
        print(f"the trend down is {trend_down}")
        
        # 综合信号
        if macd_cross_up and rsi_oversold and trend_up:
            return 1
        elif macd_cross_down and rsi_overbought and trend_down:
            return -1
        return 0
    
    def execute_trade(self, signal):
        """执行交易"""
        if signal == 0 or signal == self.last_signal:
            return
            
        try:
            if signal == 1 and self.position <= 0:  # 买入信号
                trade = self.ib.placeOrder(
                    self.contract,
                    MarketOrder('BUY', 100)
                )
                self.position = 100
                print(f"买入订单执行: {datetime.now()}")
                
            elif signal == -1 and self.position >= 0:  # 卖出信号
                trade = self.ib.placeOrder(
                    self.contract,
                    MarketOrder('SELL', 100)
                )
                self.position = -100
                print(f"卖出订单执行: {datetime.now()}")
                
            self.last_signal = signal
            
        except Exception as e:
            print(f"交易执行失败: {e}")
    
    def run(self, interval_seconds=300):
        """
        运行交易系统
        :param interval_seconds: 检查间隔(秒)
        """
        print("交易系统启动...")
        print("实时监控市场中...")
        
        while self.is_running:
            try:
                # 获取并分析指标
                print("获取并分析指标")
                indicators = self.get_indicators()
                signal = self.analyze_market(indicators)
                print(signal)
                
                # 执行交易
                self.execute_trade(signal)
                
                # 等待下一个周期
                for _ in range(interval_seconds):
                    if not self.is_running:
                        break
                    
                print("sleep")
                time.sleep(1)
                    
            except Exception as e:
                print(f"系统运行错误: {e}")
                if self.is_running:
                    time.sleep(interval_seconds)
    
    def __del__(self):
        """清理连接"""
        if self.ib.isConnected():
            self.ib.disconnect()

# 使用示例
if __name__ == "__main__":
    system = TradingSystem("AAPL")
    system.run()