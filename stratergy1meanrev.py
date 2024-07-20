import pandas as pd
import yfinance as yfin
import datetime
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

def stratergy(ticker):
    # Override yfinance's pdr to enable historical data fetching
    # yfin.pdr_override()

    # Define the date range and stock ticker
    start_date = datetime.datetime(2018, 10, 1)
    end_date = datetime.datetime(2024, 1, 1)
    ticker = ticker  # Stock ticker

    # Fetch historical price data
    data = yfin.download(ticker, start=start_date, end=end_date)

    # Ensure the index is a DatetimeIndex
    data.index = pd.to_datetime(data.index)

    # Fetch S&P 500 data to use as the risk-free rate proxy
    sp500_data = yfin.download('^GSPC', start=start_date, end=end_date)
    sp500_data['Daily Return'] = sp500_data['Close'].pct_change()
    sp500_annualized_return = sp500_data['Daily Return'].mean() * 252

    # Initialize a list to store profits for different window sizes and signal thresholds
    profits = []

    # Loop over different window sizes and signal thresholds
    for window in range(1, 100):
        for signal_threshold in range(0, 10):
            # Calculate the moving average
            data['MovingAverage'] = data['Close'].rolling(window=window).mean()

            # Implement the strategy: Buy when price is above the mean by a certain range, sell when below
            signals = data['Close'] - data['MovingAverage']
            data['Signal'] = 0
            holding = False

            for i in range(len(data)):
                if signals.iloc[i] < -signal_threshold and not holding:  # Buy signal
                    data.at[data.index[i], 'Signal'] = 1
                    holding = True
                elif signals.iloc[i] > signal_threshold and holding:  # Sell signal
                    data.at[data.index[i], 'Signal'] = -1
                    holding = False

            # Determine buy/sell points
            data['Buy'] = np.where(data['Signal'] == 1, data['Close'], np.nan)
            data['Sell'] = np.where(data['Signal'] == -1, data['Close'], np.nan)

            # Calculate profits
            data['Profit'] = data['Signal'].shift(1) * (data['Close'].diff())

            # Calculate cumulative profit
            if data['Profit'].empty:
                total_profit = 0
            else:
                data['CumulativeProfit'] = data['Profit'].cumsum()
                total_profit = data['CumulativeProfit'].iloc[-1] if not data['CumulativeProfit'].empty else 0

            profits.append((window, signal_threshold, total_profit))

    # Find the best window size and signal threshold for maximum profit
    if profits:
        best_window, best_signal_threshold, best_profit = max(profits, key=lambda x: x[2])

        # Recalculate and plot the best window size and signal threshold
        data['MovingAverage'] = data['Close'].rolling(window=best_window).mean()
        signals = data['Close'] - data['MovingAverage']
        data['Signal'] = 0
        holding = False

        for i in range(len(data)):
            if signals.iloc[i] < -best_signal_threshold and not holding:  # Buy signal
                data.at[data.index[i], 'Signal'] = 1
                holding = True
            elif signals.iloc[i] > best_signal_threshold and holding:  # Sell signal
                data.at[data.index[i], 'Signal'] = -1
                holding = False

        data['Buy'] = np.where(data['Signal'] == 1, data['Close'], np.nan)
        data['Sell'] = np.where(data['Signal'] == -1, data['Close'], np.nan)

        data['Profit'] = data['Signal'].shift(1) * (data['Close'].diff())
        data['CumulativeProfit'] = data['Profit'].cumsum()

        # Calculate annualized return, volatility, and Sharpe ratio
        trading_days = 252  # Number of trading days in a year
        annualized_return = data['Profit'].mean() * trading_days
        annualized_volatility = data['Profit'].std() * np.sqrt(trading_days)
        sharpe_ratio = (annualized_return - sp500_annualized_return) / annualized_volatility

        # Plot stock price and buy/sell signals
        # plt.figure(figsize=(14, 7))
        # plt.plot(data.index, data['Close'], label='Stock Price')
        # plt.plot(data.index, data['MovingAverage'], label='Moving Average', alpha=0.7)
        # plt.scatter(data.index, data['Buy'], label='Buy Signal', marker='^', color='green', alpha=1)
        # plt.scatter(data.index, data['Sell'], label='Sell Signal', marker='v', color='red', alpha=1)
        # plt.title(f'Stock Price with Buy/Sell Signals - Mean Reversion (Best Window: {best_window} Days, Signal Threshold: {best_signal_threshold})')
        # plt.xlabel('Date')
        # plt.ylabel('Price')
        # plt.legend()
        # st.pyplot(plt)
        # plt.show()

        fig1 = plt.figure(figsize=(14, 7))

        # Plot the stock price
        plt.plot(data.index, data['Close'], label='Stock Price')

        # Plot the moving average
        plt.plot(data.index, data['MovingAverage'], label='Moving Average', alpha=0.7)

        # Plot the buy and sell signals
        plt.scatter(data.index, data['Buy'], label='Buy Signal', marker='^', color='green', alpha=1)
        plt.scatter(data.index, data['Sell'], label='Sell Signal', marker='v', color='red', alpha=1)

        # Set title and labels
        plt.title(f'Stock Price with Buy/Sell Signals - Mean Reversion (Best Window: {best_window} Days, Signal Threshold: {best_signal_threshold})')
        plt.xlabel('Date')
        plt.ylabel('Price')

        # Add legend
        plt.legend()

        # Store the figure in a variable
        graph1 = fig1

        # Plot cumulative profit
        # plt.figure(figsize=(14, 7))
        # plt.plot(data.index, data['CumulativeProfit'], label='Cumulative Profit', color='blue')
        # plt.title(f'Cumulative Profit over Time - Mean Reversion (Best Window: {best_window} Days, Signal Threshold: {best_signal_threshold})')
        # plt.xlabel('Date')
        # plt.ylabel('Cumulative Profit')
        # plt.legend()
        # st.pyplot(plt)
        # plt.show()
        fig2 = plt.figure(figsize=(14, 7))

        # Plot the cumulative profit
        plt.plot(data.index, data['CumulativeProfit'], label='Cumulative Profit', color='blue')

        # Set title and labels
        plt.title(f'Cumulative Profit over Time - Mean Reversion (Best Window: {best_window} Days, Signal Threshold: {best_signal_threshold})')
        plt.xlabel('Date')
        plt.ylabel('Cumulative Profit')

        # Add legend
        plt.legend()

        # Store the figure in a variable
        graph2 = fig2

        conclusion_t = (f'Best Window Size: {best_window} days, Signal Threshold: {best_signal_threshold}, Cumulative Profit: {best_profit}', f'Annualized Return: {annualized_return:.2f}', f'Annualized Volatility: {annualized_volatility:.2f}', f'Sharpe Ratio: {sharpe_ratio:.2f}')
        return ({"Name": "Mean Reversion", "Best Window": best_window, "Signal Threshold": round(float(best_signal_threshold), 4), "Cumulative Profit": round(float(best_profit), 4), "Annualized Return": round(float(annualized_return), 4), "Annualized Volatility": round(float(annualized_volatility), 4), "Sharpe Ratio": round(float(sharpe_ratio), 4)}, graph1, graph2)
        return conclusion_t
        # # Output the best window size, signal range, and corresponding metrics
        # print(f'Best Window Size: {best_window} days, Signal Threshold: {best_signal_threshold}, Cumulative Profit: {best_profit}')
        # print(f'Annualized Return: {annualized_return:.2f}')
        # print(f'Annualized Volatility: {annualized_volatility:.2f}')
        # print(f'Sharpe Ratio: {sharpe_ratio:.2f}')
    else:
        conclusion_t = ({"Name": "Mean Reversion", "Best Window": None, "Signal Threshold": None, "Cumulative Profit": None, "Annualized Return": None, "Annualized Volatility": None, "Sharpe Ratio": None}, graph1, graph2)
        
        return conclusion_t

# print(stratergy("AAPL"))
# print(stratergy("TSLA"))
