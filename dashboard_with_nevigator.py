import streamlit as st
import yfinance as yfin
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt

# User Guidelines
st.sidebar.title("User Guidelines")
ticker_list = ["AAPL", "ORCL", "MSFT", "CSCO", "QCOM", "TSLA", "IBM", "GOOGL", "META", "NVDA", "AMZN"]
st.write("If stock not in options add by input below")
add_tick = st.text_input(label="Add stock, enter ticker")

if add_tick:
    ticker_list.append(add_tick)

selected_tickers = st.multiselect(label="Select Stocks TO COMPARE", options=ticker_list)
start_date = st.date_input(label="Start Date FOR PAST PRICES", value=dt.datetime.now().date() - dt.timedelta(weeks=1))
end_date = st.date_input(label="End DATE FOR PAST PRICES")

selected_all_data = yfin.download(selected_tickers, start_date, end_date) if selected_tickers else None

# Navigation Bar
st.sidebar.title("Navigation")
st.sidebar.markdown("[Trailing P/E](#trailing-pe)")
st.sidebar.markdown("[Forward P/E](#forward-pe)")
st.sidebar.markdown("[Dividend Rates](#dividend-rates)")
st.sidebar.markdown("[Beta](#beta)")
st.sidebar.markdown("[Market Capitalization](#market-capitalization)")
st.sidebar.markdown("[Full Time Employees](#full-time-employees)")
st.sidebar.markdown("[Year Low](#year-low)")
st.sidebar.markdown("[Year High](#year-high)")

def create_table_from_info_data(field):
    datalist = []
    for ticker in selected_tickers:
        ticker_info = yfin.Ticker(ticker)
        try:
            fieldinfo = ticker_info.info[field]
        except KeyError:
            fieldinfo = None
        datalist.append(fieldinfo)
    df = pd.DataFrame(datalist, index=selected_tickers, columns=["Value"])
    st.table(df)
    return df

def put_button_and_graph(data, field):
    with st.expander(":rainbow[Graph]", icon="💹"):
        st.scatter_chart(data)
        st.bar_chart(data)

def button_for_binfo(name, info):
    with st.expander(f"What is {name}?", icon="❓"):
        st.markdown(name + " is " + info)

def button_for_minfo(name, info, image):
    with st.expander(f"How to evaluate {name}", icon="⁉️"):
        st.markdown(info)
        st.image(image, width=100)

if selected_all_data is not None:
    st.write("Tabulized data")
    st.table(selected_all_data.head())

    closing_data = selected_all_data['Close']
    st.write("Closing data graph")
    st.line_chart(closing_data)

    st.markdown('<a id="trailing-pe"></a>', unsafe_allow_html=True)
    st.write("Trailing P/E")
    data = create_table_from_info_data("trailingPE")
    put_button_and_graph(data, "trailingPE")
    button_for_binfo("Trailing P/E",
                     """a relative valuation multiple that is based on the last 12 months of actual earnings.
                       It is calculated by taking the current stock price and dividing it by
                       the trailing earnings per share (EPS) for the past 12 months.""")
    button_for_minfo("Trailing P/E", "20-25", "https://www.investopedia.com/thmb/hgAHxNw5ETOZQVBlGF7WQH50Pjo=/750x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/Term-Definitions_Trailing-price-to-earnings---RECIRC-blue-009ebaf051bf4d45bb4583bd4d67c12f.jpg")

    st.markdown('<a id="forward-pe"></a>', unsafe_allow_html=True)
    st.write('Forward P/E')
    data = create_table_from_info_data("forwardPE")
    put_button_and_graph(data, "forwardPE")
    button_for_binfo("Future P/E",
                     """a valuation metric that uses earnings forecasts to
                       calculate the ratio of the share price to projected earnings per share.
                       It divides the current share price of a company
                       by the estimated future (“forward”) earnings per share (EPS) of that company.""")

    st.markdown('<a id="dividend-rates"></a>', unsafe_allow_html=True)
    st.write("Dividend Rates")
    data = create_table_from_info_data('dividendRate')
    put_button_and_graph(data, 'dividendRate')
    button_for_binfo("Dividend Rates",
                     """a financial ratio that shows how much a company pays
                       out in dividends each year relative to its stock price.""")

    st.markdown('<a id="beta"></a>', unsafe_allow_html=True)
    st.write(":rainbow[Beta]")
    data = create_table_from_info_data('beta')
    put_button_and_graph(data, "beta")
    button_for_binfo("Beta", "a measure of volatility of the stock compared to the market as a whole(usually S&P500)")

    st.markdown('<a id="market-capitalization"></a>', unsafe_allow_html=True)
    st.write("Market Capitalization")
    data = create_table_from_info_data('marketCap')
    put_button_and_graph(data, "marketCap")
    button_for_binfo("Market Cap",
                     "aka market cap, shows how much a company is worth as determined by the total market value of all outstanding shares")

    st.markdown('<a id="full-time-employees"></a>', unsafe_allow_html=True)
    st.write("Full Time Employees")
    data = create_table_from_info_data("fullTimeEmployees")
    put_button_and_graph(data, "fullTimeEmployees")

    st.markdown('<a id="year-low"></a>', unsafe_allow_html=True)
    st.write("Year Low")
    data = create_table_from_info_data('fiftyTwoWeekLow')
    put_button_and_graph(data, "fiftyTwoWeekLow")
    button_for_binfo("Year Low/ Fifty-two week Low", "the highest price at which an asset has been traded over the prior 52 weeks")

    st.markdown('<a id="year-high"></a>', unsafe_allow_html=True)
    st.write("Year High")
    create_table_from_info_data('fiftyTwoWeekHigh')
    put_button_and_graph(data, "fiftyTwoWeekHigh")
    button_for_binfo("Year High/ Fifty-two week High", "the highest price at which an asset has been traded over the prior 52 weeks")
