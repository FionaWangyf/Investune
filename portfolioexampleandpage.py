from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
import yfinance as yf
import numpy as np 
import pandas as pd
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')
import streamlit as st
import datetime as dt

st.title("Portfolio Optimizer and Simulator")

tickers = ["AAPL", "MSFT", "GOOG", "AMZN", "TSLA"]

ticker_list = ["AAPL", "ORCL", "MSFT","CSCO", "QCOM", "TSLA", "IBM", "GOOGL", "META", "NVDA", "AMZN"]

st.write("If stock not in options add by input below")
add_tick = st.text_input(label="Add stock, enter ticker")

if add_tick:
    ticker_list.append(add_tick)

start_date = st.date_input(label="Start Date FOR PAST PRICES", value=dt.datetime.now().date() - dt.timedelta(weeks=20))
end_date = st.date_input(label="End DATE FOR PAST PRICES")
print(end_date - start_date)
if not end_date - start_date > dt.timedelta(weeks=9):
    st.warning("Start Date CANNOT be after END date and :orange[difference must be more than 3 months].")
    st.stop()

selected_tickers = st.multiselect(label="Select Stocks TO add to portfolio builder", options=ticker_list)

if len(selected_tickers) > 1:
    data = yf.download(selected_tickers, start=start_date, end=end_date)["Adj Close"]
    st.subheader("Tabulized Past Data")
    st.table(data.head())
    data.fillna(method='ffill', inplace=True)
    st.subheader("A moving average plot of 3 months for all stocks in our portfolio")
    st.line_chart(data.rolling(63).mean())
    st.header("Data Correlation")
    st.table(data.corr())
    
    # 将解释内容放入expander中
    with st.expander("Correlation Explanation"):
        st.write("""
            Correlation is a measurement between -1 and 1, which indicates the linear relationship between two variables.
            If there is no relationship between two variables, the correlation coefficient is 0.
            If there is a perfect relationship, the correlation is 1.
            And if there is a perfect inverse relationship, the correlation is -1.
        """)
    
    # Calculate expected returns and sample covariance
    try:
        mu = expected_returns.mean_historical_return(data, frequency=126)
        S = risk_models.sample_cov(data)

        # Optimize for maximal Sharpe ratio
        ef = EfficientFrontier(mu, S)
        raw_weights = ef.max_sharpe()
        cleaned_weights = ef.clean_weights()
        clean_dic = dict(cleaned_weights)
        print(clean_dic)
        
        # 创建DataFrame时使用正确的索引
        dataframe = pd.DataFrame(list(clean_dic.values()), index=clean_dic.keys(), columns=['SUGGESTED WEIGHTS'])
        st.subheader("PORTFOLIO SUGGESTED WEIGHTS")
        st.write("The suggested portfolio weighting means the weight to put money into each stock")
        st.table(dataframe)
        print(dataframe)

        # 打印并显示投资组合的绩效指标
        expected_annual_return, annual_volatility, sharpe_ratio = ef.portfolio_performance(verbose=True)
        st.subheader("PORTFOLIO PERFORMANCE")
        st.write(f"Expected annual return: {expected_annual_return*100:.1f}%")
        st.write(f"Annual volatility: {annual_volatility*100:.1f}%")
        st.write(f"Sharpe Ratio: {sharpe_ratio:.2f}")

    except ValueError:
        st.write("Can't put these stocks in Portfolio all returns too low, try re-considering the stocks.")
        with st.expander("Need Help?"):
            st.write("Need Help analyzing stocks? Use our chatbot")
            st.write("Need help comparing stocks? Use our stock comparer")
    
    else:
        latest_prices = get_latest_prices(data)
        print("Cleaned Weights:", cleaned_weights)
        print("Latest Prices:", latest_prices)
    
        st.subheader("Enter the initial investment value:")
        initial_investment = st.number_input("", min_value=500, value=100000, step=1000)
        print("Initial Investment:", initial_investment)

        if initial_investment:
            da = DiscreteAllocation(cleaned_weights, latest_prices, total_portfolio_value=initial_investment)
            allocation, leftover = da.greedy_portfolio()
            print(allocation)
            print(allocation.values())
            
            # 创建DataFrame时使用正确的索引和列名
            allocationdf = pd.DataFrame(list(allocation.values()), index=allocation.keys(), columns=['Shares'])
            st.table(allocationdf)
            st.write(f"Funds remaining: {round(float(leftover), 2)}")
            print("Discrete allocation:", allocation)
            print("Funds remaining: Rs.{:.2f}".format(leftover))

else:
    st.stop()
    st.write("Need more than one stock to have a Portfolio.")
