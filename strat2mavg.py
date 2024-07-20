import pandas as pd
import yfinance as yfin
import datetime
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
yfin.pdr_override()

# 获取历史价格数据
def stratergy(ticker):
    start_date = datetime.datetime(2018, 10, 1)
    end_date = datetime.datetime(2024, 1, 1)
    ticker = ticker  # 股票代码，可以更改为其他股票
    data = yfin.download(ticker, start=start_date, end=end_date)

    # 确保索引为DatetimeIndex
    data.index = pd.to_datetime(data.index)

    # 获取3个月美国国债收益率作为无风险利率
    t_bill_data = yfin.download('^IRX', start=start_date, end=end_date)
    t_bill_rate = t_bill_data['Close'][-1] / 100  # 转换为百分比

    # 存储不同窗口大小和信号范围的累计利润
    profits = []

    # 调整窗口大小范围和信号范围
    for window in range(1, 51, 5):
        for signal_threshold in range(2, 11):
            # 计算移动平均
            data['MovingAverage'] = data['Close'].rolling(window=window).mean()

            # 策略实施：当价格高于均值一定范围时买入，低于均值一定范围时卖出
            signals = data['Close'] - data['MovingAverage']
            data['Signal'] = 0
            holding = False

            for i in range(len(data)):
                if signals.iloc[i] > -signal_threshold and not holding:  # 买入信号
                    data.at[data.index[i], 'Signal'] = 1
                    holding = True
                elif signals.iloc[i] < signal_threshold and holding:  # 卖出信号
                    data.at[data.index[i], 'Signal'] = -1
                    holding = False

            # 确定买卖时间点
            data['Buy'] = np.where(data['Signal'] == 1, data['Close'], np.nan)
            data['Sell'] = np.where(data['Signal'] == -1, data['Close'], np.nan)

            # 计算利润
            data['Profit'] = data['Signal'].shift(1) * (data['Close'].diff())

            # 计算累计利润
            if data['Profit'].empty:
                total_profit = 0
            else:
                data['CumulativeProfit'] = data['Profit'].cumsum()
                total_profit = data['CumulativeProfit'].iloc[-1] if not data['CumulativeProfit'].empty else 0

            profits.append((window, signal_threshold, total_profit))

    # 找出利润最高的窗口大小和信号范围
    if profits:
        best_window, best_signal_threshold, best_profit = max(profits, key=lambda x: x[2])

        # 重新计算并绘制最佳窗口大小和信号范围的图表
        data['MovingAverage'] = data['Close'].rolling(window=best_window).mean()
        signals = data['Close'] - data['MovingAverage']
        data['Signal'] = 0
        holding = False

        for i in range(len(data)):
            if signals.iloc[i] > -best_signal_threshold and not holding:  # 买入信号
                data.at[data.index[i], 'Signal'] = 1
                holding = True
            elif signals.iloc[i] < best_signal_threshold and holding:  # 卖出信号
                data.at[data.index[i], 'Signal'] = -1
                holding = False

        data['Buy'] = np.where(data['Signal'] == 1, data['Close'], np.nan)
        data['Sell'] = np.where(data['Signal'] == -1, data['Close'], np.nan)

        data['Profit'] = data['Signal'].shift(1) * (data['Close'].diff())
        data['CumulativeProfit'] = data['Profit'].cumsum()

        # 计算年化收益率、波动率和Sharpe比率
        trading_days = 252  # 每年的交易天数
        annualized_return = data['Profit'].mean() * trading_days
        annualized_volatility = data['Profit'].std() * np.sqrt(trading_days)
        sharpe_ratio = (annualized_return - t_bill_rate) / annualized_volatility

        # 绘制股票价格曲线和买卖时间点
        fig = plt.figure(figsize=(14, 7))
        plt.plot(data.index, data['Close'], label='Stock Price')
        plt.plot(data.index, data['MovingAverage'], label='Moving Average', alpha=0.7)
        plt.scatter(data.index, data['Buy'], label='Buy Signal', marker='^', color='green', alpha=1)
        plt.scatter(data.index, data['Sell'], label='Sell Signal', marker='v', color='red', alpha=1)
        plt.title(f'Stock Price with Buy/Sell Signals - Mean Reversion (Best Window: {best_window} Days, Signal Threshold: {best_signal_threshold})')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        # st.pyplot(plt)
        graph1 = fig
        # plt.show()

        # 绘制利润图
        fig2 = plt.figure(figsize=(14, 7))
        plt.plot(data.index, data['CumulativeProfit'], label='Cumulative Profit', color='blue')
        plt.title(f'Cumulative Profit over Time - Moving Average (Best Window: {best_window} Days, Signal Threshold: {best_signal_threshold})')
        plt.xlabel('Date')
        plt.ylabel('Cumulative Profit')
        plt.legend()
        graph2 = fig2
        # st.pyplot(plt)
        # plt.show()

        # 输出最佳窗口大小、信号范围和对应的指标
        # print(f'Best Window Size: {best_window} days，Signal Threshold: {best_signal_threshold}，Cumulative Profit: {best_profit}')
        # print(f'Annualized Return: {annualized_return:.2f}')
        # print(f'Annualized Volatility: {annualized_volatility:.2f}')
        # print(f'Sharpe Ratio: {sharpe_ratio:.2f}')
        conclut = {"Name":"Moving Average", "Best Window": best_window, "Signal Threshold": best_signal_threshold, "Cumulative Profit": round(float(best_profit), 4), "Annualized Return": round(float(annualized_return), 4), "Annualized Volatility": round(float(annualized_volatility), 4) , "Sharpe Ratio": round(float(sharpe_ratio),4)}
        return (conclut, graph1, graph2)
    else:
        return ({"Name":"Moving Average", "Best Window": None, "Signal Threshold": None, "Cumulative Profit": None, "Annualized Return": None, "Annualized Volatility": None , "Sharpe Ratio": None}, graph1, graph2)
        

# print(stratergy("AAPL"))

# print(stratergy("TSLA"))
