import stratergy1meanrev as mrev_m
import strat2mavg as mavg_m
import strat3rsi as rsi_m
import strat4cndst as cndst_m
import matplotlib.pyplot as plt
import streamlit as st



ticker=None



def run_strats(ticker):
    mrev, mrevfig1, mrevfig2 = mrev_m.stratergy(ticker)
    mavg, mavgfig1, mavgfig2 = mavg_m.stratergy(ticker)
    rsi, rsifig1, rsifig2, rsifig3 = rsi_m.stratergy(ticker)
    cndst ,cndstfig1 ,cndstfig2 = cndst_m.stratergy(ticker)
    print(mrev, mavg, rsi, cndst)
    return [mrev, mavg, rsi, cndst], [mrevfig1, mrevfig2, mavgfig1, mavgfig2, rsifig1, rsifig2, rsifig3, cndstfig1, cndstfig2]





import pandas as pd

# Define the dictionaries
# mrev = {"Name":"Mean Reversion", 'Best Window': 3, 'Signal Threshold': 2.0, 'Cumulative Profit': 70.455, 'Annualized Return': 13.4505, 'Annualized Volatility': 13.8381, 'Sharpe Ratio': 0.9636}
# mavg = {"Name": "Moving Average", 'Best Window': 16, 'Signal Threshold': 10, 'Cumulative Profit': 226.1652, 'Annualized Return': 43.177, 'Annualized Volatility': 35.7679, 'Sharpe Ratio': 1.2057}
# rsi = {"Name":"RSI", 'Best RSI Period': 5, 'Buy Threshold': 40, 'Sell Threshold': 60, 'Cumulative Profit': 26.0124, 'Annualized Return': 4.966, 'Annualized Volatility': 13.6242, 'Sharpe Ratio': 0.3607}
# cndst = {'Name': 'Candlestick Bollinger Bands', 'Best Window Size': 100, 'Best Std Multiplier': 1.3, 'Cumulative Profit': 25, 'Annualized Return': 5, 'Annualized Volatility': 7, 'Sharpe Ratio': 0.7122}

# Combine the dictionaries into a list
# strategies = [mrev, mavg, rsi, cndst]






def get_analysis(ticker, data):
    stratergies ,figures = data
    # print(stratergies)

    # stratergies = [{'Name': 'Mean Reversion', 'Best Window': 3, 'Signal Threshold': 2.0, 'Cumulative Profit': 70.455, 'Annualized Return': 13.4505, 'Annualized Volatility': 13.8381, 'Sharpe Ratio': 0.9636}, {'Name': 'Moving Average', 'Best Window': 16, 'Signal Threshold': 10, 'Cumulative Profit': 226.1652, 'Annualized Return': 43.177, 'Annualized Volatility': 35.7679, 'Sharpe Ratio': 1.2057}, {'Name': 'RSI', 'Best RSI Period': 5, 'Buy Threshold': 40, 'Sell Threshold': 60, 'Cumulative Profit': 26.0124, 'Annualized Return': 4.966, 'Annualized Volatility': 13.6242, 'Sharpe Ratio': 0.3607}, {'Name': 'Candelstick Bollinger Bands', 'Best Window Size': 100, 'Best Std Multiplier': 1.3, 'Cumulative Profit': 25, 'Annualized Return': 5, 'Annualized Volatility': 7, 'Sharpe Ratio': 0.7122}]

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(stratergies)

    # Define the conditions for analysis
    conditions = [
        {
            "metric": "Cumulative Profit",
            "highest": df.loc[df['Cumulative Profit'].idxmax()],
            "lowest": df.loc[df['Cumulative Profit'].idxmin()],
            "interpretation": "The {} strategy significantly outperformed other strategies in terms of cumulative profit. This suggests it was able to capture more profitable opportunities over the period analyzed."
        },
        {
            "metric": "Annualized Return",
            "highest": df.loc[df["Annualized Return"].idxmax()],
            "lowest": df.loc[df["Annualized Return"].idxmin()],
            "interpretation": "The {} strategy also has the highest annualized return, indicating it provided the most significant growth rate over time. The {} strategy had the lowest annualized return, indicating less overall growth."
        },
        {
            "metric": "Annualized Volatility",
            "highest": df.loc[df["Annualized Volatility"].idxmax()],
            "lowest": df.loc[df["Annualized Volatility"].idxmin()],
            "interpretation": "Higher volatility indicates more fluctuation in returns. While the {} strategy yielded the highest returns, it also came with the highest risk. The {} strategy had the least fluctuation, indicating a more stable return profile."
        },
        {
            "metric": "Sharpe Ratio",
            "highest": df.loc[df["Sharpe Ratio"].idxmax()],
            "lowest": df.loc[df["Sharpe Ratio"].idxmin()],
            "interpretation": "The Sharpe Ratio measures risk-adjusted return. The {} strategy not only provided high returns but also had a good balance of risk, as reflected in its highest Sharpe Ratio. The {} strategy had the lowest Sharpe Ratio, indicating poor risk-adjusted performance."
        }
    ]

    # Generate the detailed analysis
    analysis = "### Analysis of Key Metrics\n\n"

    for condition in conditions:
        metric = condition["metric"]
        highest = condition["highest"]
        lowest = condition["lowest"]
        interpretation = condition["interpretation"].format(highest["Name"], lowest["Name"])
        
        analysis += f"#### {metric}\n\n"
        analysis += f"* **Highest:** {highest['Name']} ({highest[metric]})\n"
        analysis += f"* **Lowest:** {lowest['Name']} ({lowest[metric]})\n"
        analysis += f"* **Interpretation:** {interpretation}\n\n"

    return analysis




def max_prof(ticker, data):
    strategies, graphs = data
    # Find the strategy with the highest cumulative profit
    max_profit_strategy = max(strategies, key=lambda x: x['Cumulative Profit'])
    # Get the index of the max profit strategy to return the corresponding graphs
    index = strategies.index(max_profit_strategy)
    return give_all_data_in_format(*get_strat_data_and_graph(max_profit_strategy, graphs))


def get_strat_data_and_graph(stratergy, graphs):
    # Each strategy may have a different number of graphs, so we need to slice accordingly
    strategy_graphs = []
    if stratergy['Name'] == 'Mean Reversion':
        strategy_graphs = graphs[0:2]
    elif stratergy['Name'] == 'Moving Average':
        strategy_graphs = graphs[2:4]
    elif stratergy['Name'] == 'RSI':
        strategy_graphs = graphs[4:7]
    elif stratergy['Name'] == 'Candlestick Bollinger Bands':
        strategy_graphs = graphs[7:9]

    return stratergy, strategy_graphs

def high_sharpe_ratio(ticker, data):
    strategies, graphs = data
    highest_sharpe_ratio = max(strategies, key=lambda x: x['Sharpe Ratio'])
    index = strategies.index(highest_sharpe_ratio)
    return give_all_data_in_format(*get_strat_data_and_graph(highest_sharpe_ratio, graphs))

def less_risk_only(ticker, data):
    strategies, graphs = data
    least_risk_strategy = min(strategies, key=lambda x: x['Annualized Volatility'])
    index = strategies.index(least_risk_strategy)
    return give_all_data_in_format(*get_strat_data_and_graph(least_risk_strategy, graphs))

# mrev = {"Name":"Mean Reversion", 'Best Window': 3, 'Signal Threshold': 2.0, 'Cumulative Profit': 70.455, 'Annualized Return': 13.4505, 'Annualized Volatility': 13.8381, 'Sharpe Ratio': 0.9636}
# mavg = {"Name": "Moving Average", 'Best Window': 16, 'Signal Threshold': 10, 'Cumulative Profit': 226.1652, 'Annualized Return': 43.177, 'Annualized Volatility': 35.7679, 'Sharpe Ratio': 1.2057}
# rsi = {"Name":"RSI", 'Best RSI Period': 5, 'Buy Threshold': 40, 'Sell Threshold': 60, 'Cumulative Profit': 26.0124, 'Annualized Return': 4.966, 'Annualized Volatility': 13.6242, 'Sharpe Ratio': 0.3607}
# cndst = {'Name': 'Candlestick Bollinger Bands', 'Best Window Size': 100, 'Best Std Multiplier': 1.3, 'Cumulative Profit': 25, 'Annualized Return': 5, 'Annualized Volatility': 7, 'Sharpe Ratio': 0.7122}

def give_all_data_in_format(strategy, graphs):
    all_data = f"""### {strategy['Name']} Strategy\n\n  """
    if strategy['Name'] == 'Mean Reversion':
        all_data += f'Best Window: {strategy["Best Window"]}\n  '
        all_data += f'Signal Threshold: {strategy["Signal Threshold"]}\n  ' 

    elif strategy['Name'] == 'Moving Average':
        all_data += f'Best Window: {strategy["Best Window"]}\n  '
        all_data += f'Signal Threshold: {strategy["Signal Threshold"]}\n  '
        
    elif strategy['Name'] == 'RSI':
        all_data += f'Best RSI Period: {strategy["Best RSI Period"]}\n  '
        all_data += f'Buy Threshold: {strategy["Buy Threshold"]}\n  '
        all_data += f'Sell Threshold: {strategy["Sell Threshold"]}\n  '

    elif strategy['Name'] == 'Candlestick Bollinger Bands':
        all_data += f'Best Window Size: {strategy["Best Window Size"]}\n  '
        all_data += f'Best Std Multiplier: {strategy["Best Std Multiplier"]}\n  '
    
    all_data += f'Cumulative Profit: {strategy["Cumulative Profit"]}\n  '
    all_data += f'Annualized Return: {strategy["Annualized Return"]}\n  '
    all_data += f'Annualized Volatility: {strategy["Annualized Volatility"]}\n  '
    all_data += f'Sharpe Ratio: {strategy["Sharpe Ratio"]}\n  '

    return all_data, graphs

def plot_graphs(graphs):
    for fig in graphs:
        if isinstance(fig, plt.Figure):
            st.pyplot(fig)
        else:
            st.warning("The provided object is not a valid Matplotlib Figure")

#     strategies = [mrev, mavg, rsi, cndst]
#     df = pd.DataFrame(strategies)
    
#     # Find the strategy with the highest cumulative profit
#     max_profit_strategy = df.loc[df['Cumulative Profit'].idxmax()]
#     print(f"Max Profit Strategy: {max_profit_strategy['Name']}")
#     print(max_profit_strategy)
    
#     return max_profit_strategy

# # def less_risk__bprof(mrev, mavg, rsi, cndst):
# #     return less_risk__bprof

