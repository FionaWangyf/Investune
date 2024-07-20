import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yfin
import datetime
import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
import streamlit as st
# import statsmodels.api as sm

yfin.pdr_override()
def stratergy(ticker):
    # 获取历史价格数据
    start_date = datetime.datetime(2018, 10, 1)
    end_date = datetime.datetime(2024, 1, 1)
    ticker = ticker  # 股票代码，可以更改为其他股票
    data = pdr.get_data_yahoo(ticker, start=start_date, end=end_date)

    # 确保索引为DatetimeIndex
    data.index = pd.to_datetime(data.index)

    # 存储不同窗口大小和标准差倍数的累计利润
    profits = []

    # 调整窗口大小范围和标准差倍数范围
    for window in range(1, 20):  # 窗口大小范围
        for std_multiplier in np.arange(1.0, 3.1, 0.1):  # 标准差倍数范围
            # 计算布林带
            data['SMA'] = data['Close'].rolling(window=window * 20, min_periods=1).mean()  # 窗口大小调整为20倍
            data['STD'] = data['Close'].rolling(window=window * 20, min_periods=1).std()
            data['Upper'] = data['SMA'] + (data['STD'] * std_multiplier)
            data['Lower'] = data['SMA'] - (data['STD'] * std_multiplier)

            # 生成买卖信号，只有在满足条件时才进行买卖操作
            holding = False
            signals = []
            for i in range(len(data)):
                if data['Close'].iloc[i] < data['Lower'].iloc[i]:
                    if not holding:  # 只有在没有持仓时才能买入
                        signals.append(1)
                        holding = True
                    else:
                        signals.append(0)
                elif data['Close'].iloc[i] > data['Upper'].iloc[i]:
                    if holding:  # 只有在持仓时才能卖出
                        signals.append(-1)
                        holding = False
                    else:
                        signals.append(0)
                else:
                    signals.append(0)

            data['Signal'] = signals

            # 计算利润
            data['Profit'] = data['Signal'].shift(1) * (data['Close'].diff())

            # 计算累计利润，避免空数组问题
            if data['Profit'].empty:
                total_profit = 0
            else:
                data['CumulativeProfit'] = data['Profit'].cumsum()
                total_profit = data['CumulativeProfit'].iloc[-1] if not data['CumulativeProfit'].empty else 0
            
            profits.append((window, std_multiplier, total_profit))

    # 找出利润最高的窗口大小和标准差倍数
    if profits:
        best_window, best_std_multiplier, best_profit = max(profits, key=lambda x: x[2])

        # 重新计算并绘制最佳窗口大小和标准差倍数的图表
        data['SMA'] = data['Close'].rolling(window=best_window * 20, min_periods=1).mean()
        data['STD'] = data['Close'].rolling(window=best_window * 20, min_periods=1).std()
        data['Upper'] = data['SMA'] + (data['STD'] * best_std_multiplier)
        data['Lower'] = data['SMA'] - (data['STD'] * best_std_multiplier)

        holding = False
        signals = []
        for i in range(len(data)):
            if data['Close'].iloc[i] < data['Lower'].iloc[i]:
                if not holding:  # 只有在没有持仓时才能买入
                    signals.append(1)
                    holding = True
                else:
                    signals.append(0)
            elif data['Close'].iloc[i] > data['Upper'].iloc[i]:
                if holding:  # 只有在持仓时才能卖出
                    signals.append(-1)
                    holding = False
                else:
                    signals.append(0)
            else:
                signals.append(0)

        data['Signal'] = signals

        data['Buy'] = np.where(data['Signal'] == 1, data['Close'], np.nan)
        data['Sell'] = np.where(data['Signal'] == -1, data['Close'], np.nan)

        data['Profit'] = data['Signal'].shift(1) * (data['Close'].diff())
        data['CumulativeProfit'] = data['Profit'].cumsum()

        # 获取当前3个月美国国债收益率作为无风险利率
        t_bill_data = pdr.get_data_yahoo("^IRX", start=start_date, end=end_date)
        t_bill_rate = t_bill_data['Close'][-1] / 100  # 转换为百分比

        # 计算年平均收益率、波动率和Sharpe比率
        annual_returns = data['Profit'].mean() * 252
        annual_volatility = data['Profit'].std() * np.sqrt(252)
        sharpe_ratio = (annual_returns - t_bill_rate) / annual_volatility

        # 转换数据格式以供mplfinance使用
        data_for_mpf = data[['Open', 'High', 'Low', 'Close']]

        # 绘制K线图和买卖时间点
        buy_signals = mpf.make_addplot(data['Buy'], type='scatter', markersize=50, marker='^', color='green', label='Buy Signal')
        sell_signals = mpf.make_addplot(data['Sell'], type='scatter', markersize=50, marker='v', color='red', label='Sell Signal')
        upper_band = mpf.make_addplot(data['Upper'], color='orange', linestyle='--', label='Upper Band')
        lower_band = mpf.make_addplot(data['Lower'], color='blue', linestyle='--', label='Lower Band')

        fig2, ax2 = mpf.plot(data_for_mpf, type='candle', style='charles', figsize=(14, 7), addplot=[buy_signals, sell_signals, upper_band, lower_band], title=f'Candlestick Chart with Buy/Sell Signals (Best Window: {best_window * 20} Days, Std Multiplier: {best_std_multiplier})', ylabel='Price', returnfig=True)
        graph1 = fig2
        # plot this in streamlit
        # st.pyplot()

        # 绘制利润图
        # plt.figure(figsize=(14, 7))
        # plt.plot(data['CumulativeProfit'], label='Cumulative Profit', color='blue')
        # # plt.title("no data.index")
        # plt.title(f'Cumulative Profit over Time - Candlesticks (Best Window: {best_window * 20} Days, Std Multiplier: {best_std_multiplier})')
        # plt.xlabel('Date')
        # plt.ylabel('Cumulative Profit')
        # plt.legend()
        # st.pyplot(plt)
        # plt.show()
        # Create the figure and axis objects
        fig, ax = plt.subplots(figsize=(14, 7))

        # Plot the cumulative profit
        ax.plot(data['CumulativeProfit'], label='Cumulative Profit', color='blue')

        # Set title and labels
        ax.set_title(f'Cumulative Profit over Time - Candlesticks (Best Window: {best_window * 20} Days, Std Multiplier: {best_std_multiplier})')
        ax.set_xlabel('Date')
        ax.set_ylabel('Cumulative Profit')

        # Add legend
        ax.legend()

        # Store the figure in a variable
        graph2 = fig

        # Show the plot
        # plt.show()

        # plt.plot(data['CumulativeProfit'], label='Cumulative Profit', color='blue')
        # plt.title("No data.index")
        # st.pyplot(plt)

        # 输出最佳窗口大小、标准差倍数和对应的指标
        # print(f'Best Window Size: {best_window * 20} days，Best Std Multiplier: {best_std_multiplier}，Cumulative Profit: {best_profit}')
        # print(f'Annualized Return: {annual_returns:.2f}')
        # print(f'Annualized Volatility: {annual_volatility:.2f}')
        # print(f'Sharpe Ratio: {sharpe_ratio:.2f}')
        return ({"Name": "Candelstick Bollinger Bands", "Best Window Size": best_window * 20, "Best Std Multiplier": round(float(best_std_multiplier),4), 
                "Cumulative Profit": round(float(best_profit)), "Annualized Return": round(float(annual_returns)), 'Annualized Volatility': round(float(annual_volatility)),
                "Sharpe Ratio": round(float(sharpe_ratio), 4)},  graph1, graph2)

    else:
        return ({"Name": "Candelstick Bollinger Bands", "Best Window Size": None, "Best Std Multiplier": None, 
                "Cumulative Profit": None, "Annualized Return": None, 'Annualized Volatility': None,
                "Sharpe Ratio": None}, graph1, graph2)
#x=stratergy("AAPL")
#plt.show(x[1])
#plt.show(x[2])

# print(stratergy("TSLA"))
