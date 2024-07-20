import pandas as pd
import yfinance as yfin
import datetime
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# Override yfinance's pdr to enable historical data fetching
yfin.pdr_override()
def stratergy(ticker):
    # Define the date range and stock ticker
    start_date = datetime.datetime(2018, 10, 1)
    end_date = datetime.datetime(2024, 1, 1)
    ticker = ticker  # Stock ticker

    # Fetch historical price data
    data = yfin.download(ticker, start=start_date, end=end_date)

    # Ensure the index is a DatetimeIndex
    data.index = pd.to_datetime(data.index)

    # Fetch 3-month US Treasury Bill data to use as the risk-free rate
    t_bill_data = yfin.download('^IRX', start=start_date, end=end_date)
    t_bill_rate = t_bill_data['Close'][-1] / 100  # Convert to a percentage

    # Function to calculate RSI
    def calculate_rsi(data, window):
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    # Initialize a list to store profits for different RSI periods and thresholds
    profits = []

    # Loop over different RSI periods and thresholds
    for rsi_period in range(5, 31, 5):
        for buy_threshold in range(20, 41, 5):
            sell_threshold = 100 - buy_threshold
            
            # Calculate the RSI
            data['RSI'] = calculate_rsi(data, rsi_period)

            # Implement the strategy: Buy when RSI is below the buy threshold, sell when RSI is above the sell threshold
            data['Signal'] = 0
            holding = False

            for i in range(len(data)):
                if data['RSI'].iloc[i] < buy_threshold and not holding:  # Buy signal
                    data.at[data.index[i], 'Signal'] = 1
                    holding = True
                elif data['RSI'].iloc[i] > sell_threshold and holding:  # Sell signal
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

            profits.append((rsi_period, buy_threshold, total_profit))

    # Find the best RSI period and thresholds for maximum profit
    if profits:
        best_rsi_period, best_buy_threshold, best_profit = max(profits, key=lambda x: x[2])
        best_sell_threshold = 100 - best_buy_threshold

        # Recalculate and plot the best RSI period and thresholds
        data['RSI'] = calculate_rsi(data, best_rsi_period)
        data['Signal'] = 0
        holding = False

        for i in range(len(data)):
            if data['RSI'].iloc[i] < best_buy_threshold and not holding:  # Buy signal
                data.at[data.index[i], 'Signal'] = 1
                holding = True
            elif data['RSI'].iloc[i] > best_sell_threshold and holding:  # Sell signal
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
        sharpe_ratio = (annualized_return - t_bill_rate) / annualized_volatility

        # Plot stock price and buy/sell signals
        # plt.figure(figsize=(14, 7))
        # plt.plot(data.index, data['Close'], label='Stock Price')
        # plt.scatter(data.index, data['Buy'], label='Buy Signal', marker='^', color='green', alpha=1)
        # plt.scatter(data.index, data['Sell'], label='Sell Signal', marker='v', color='red', alpha=1)
        # plt.title(f'Stock Price with Buy/Sell Signals - RSI Strategy (Best RSI Period: {best_rsi_period} Days, Buy Threshold: {best_buy_threshold}, Sell Threshold: {best_sell_threshold})')
        # plt.xlabel('Date')
        # plt.ylabel('Price')
        # plt.legend()
        # st.pyplot(plt)
        # plt.show()
        fig1 = plt.figure(figsize=(14, 7))

        # Plot the stock price
        plt.plot(data.index, data['Close'], label='Stock Price')

        # Plot the buy and sell signals
        plt.scatter(data.index, data['Buy'], label='Buy Signal', marker='^', color='green', alpha=1)
        plt.scatter(data.index, data['Sell'], label='Sell Signal', marker='v', color='red', alpha=1)

        # Set title and labels
        plt.title(f'Stock Price with Buy/Sell Signals - RSI Strategy (Best RSI Period: {best_rsi_period} Days, Buy Threshold: {best_buy_threshold}, Sell Threshold: {best_sell_threshold})')
        plt.xlabel('Date')
        plt.ylabel('Price')

        # Add legend
        plt.legend()

        # Store the figure in a variable
        graph1 = fig1

        # Plot RSI with buy/sell thresholds
        # plt.figure(figsize=(14, 7))
        # plt.plot(data.index, data['RSI'], label='RSI', color='purple')
        # plt.axhline(y=best_buy_threshold, color='green', linestyle='--', label='Buy Threshold')
        # plt.axhline(y=best_sell_threshold, color='red', linestyle='--', label='Sell Threshold')
        # plt.title(f'RSI with Buy/Sell Thresholds (Best RSI Period: {best_rsi_period} Days)')
        # plt.xlabel('Date')
        # plt.ylabel('RSI')
        # plt.legend()
        # st.pyplot(plt)
        # plt.show()

        # Create the figure
        fig2 = plt.figure(figsize=(14, 7))

        # Plot the RSI
        plt.plot(data.index, data['RSI'], label='RSI', color='purple')

        # Add horizontal lines for buy and sell thresholds
        plt.axhline(y=best_buy_threshold, color='green', linestyle='--', label='Buy Threshold')
        plt.axhline(y=best_sell_threshold, color='red', linestyle='--', label='Sell Threshold')

        # Set title and labels
        plt.title(f'RSI with Buy/Sell Thresholds (Best RSI Period: {best_rsi_period} Days)')
        plt.xlabel('Date')
        plt.ylabel('RSI')

        # Add legend
        plt.legend()

        # Store the figure in a variable
        graph2 = fig2

        # Plot cumulative profit
        # plt.figure(figsize=(14, 7))
        # plt.plot(data.index, data['CumulativeProfit'], label='Cumulative Profit', color='blue')
        # plt.title(f'Cumulative Profit over Time - RSI Strategy (Best RSI Period: {best_rsi_period} Days, Buy Threshold: {best_buy_threshold}, Sell Threshold: {best_sell_threshold})')
        # plt.xlabel('Date')
        # plt.ylabel('Cumulative Profit')
        # plt.legend()
        # st.pyplot(plt)
        # plt.show()
        # Create the figure
        fig3 = plt.figure(figsize=(14, 7))

        # Plot the cumulative profit
        plt.plot(data.index, data['CumulativeProfit'], label='Cumulative Profit', color='blue')

        # Set title and labels
        plt.title(f'Cumulative Profit over Time - RSI Strategy (Best RSI Period: {best_rsi_period} Days, Buy Threshold: {best_buy_threshold}, Sell Threshold: {best_sell_threshold})')
        plt.xlabel('Date')
        plt.ylabel('Cumulative Profit')

        # Add legend
        plt.legend()

        # Store the figure in a variable
        graph3 = fig3


        # Output the best RSI period, thresholds, and corresponding profit
        # print(f'Best RSI Period: {best_rsi_period} days, Buy Threshold: {best_buy_threshold}, Sell Threshold: {best_sell_threshold}, Cumulative Profit: {best_profit}')
        # print(f'Annualized Return: {annualized_return:.2f}')
        # print(f'Annualized Volatility: {annualized_volatility:.2f}')
        # print(f'Sharpe Ratio: {sharpe_ratio:.2f}')

        return ({"Name":"RSI","Best RSI Period": best_rsi_period, "Buy Threshold":best_buy_threshold, "Sell Threshold": best_sell_threshold, "Cumulative Profit": round(float(best_profit), 4), 
                "Annualized Return": round(float(annualized_return), 4),  'Annualized Volatility': round(float(annualized_volatility), 4),  "Sharpe Ratio": round(float(sharpe_ratio), 4)}, graph1, graph2, graph3)
    else:
        return ({"Name":"RSI","Best RSI Period": None, "Buy Threshold":None, "Sell Threshold": None, "Cumulative Profit": None, 
                "Annualized Return": None,  'Annualized Volatility': None,  "Sharpe Ratio": None}, graph1, graph2, graph3)

# print(stratergy("AAPL"))
# print(stratergy("TSLA"))
