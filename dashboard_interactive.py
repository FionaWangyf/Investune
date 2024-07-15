# DASHBOARD COMPARE STOCKS

import streamlit as st

import yfinance as yfin

import matplotlib.pyplot as plt

# def add_ticker():




ticker_list = ["AAPL", "ORCL", "MSFT","CSCO", "QCOM", "TSLA", "IBM", "GOOGL", "META", "NVDA", "AMZN"]

st.write("If stock not in options add by input below")
add_tick = st.text_input(label="Add stock, enter ticker")

if add_tick:
    ticker_list.append(add_tick)

selected_tickers = st.multiselect(label="Select Stocks TO COMPARE", options=ticker_list)
start_date = st.date_input(label="Start Date FOR PAST PRICES")
end_date = st.date_input(label="End DATE FOR PAST PRICES")
# print(start_date)
# print(type(start_date))
# print(str(start_date))
selected_all_data = yfin.download(selected_tickers, start_date, end_date) if selected_tickers else None
# print(selected_all_data)
# print(len(selected_all_data))
# print(type(selected_all_data))

if selected_all_data is not None:
    st.table(selected_all_data)
    closing_data = selected_all_data['Close']
    st.line_chart(closing_data)


# closing_data_graph = plt.plot(closing_data)
# st.pyplot(closing_data)

# st.multiset(label="Select Stocks", options=ticker_list, ":rainbow[options]")