# dashboard_interactive_with_expanders.py

# dashboard_interactive_wo_positioning.py

# DASHBOARD COMPARE STOCKS

import streamlit as st

import yfinance as yh

import matplotlib.pyplot as plt

import pandas as pd

import datetime as dt
# def add_ticker():


ticker_list = ["AAPL", "ORCL", "MSFT","CSCO", "QCOM", "TSLA", "IBM", "GOOGL", "META", "NVDA", "AMZN"]

data_opts = ['Trailing P/E', 'Forward P/E', 'Dividend Rate', 'Dividend Yield', 'Beta', 'Market Capitalization', 'Sector', 
             'Volume', 'Profit Margins', 'Trailing EPS', 'Forward EPS', 'PEG Ratio', 'Ebitda', 'Total Revenue',
             'Full Time Employees', 'Year Low', 'Year High', 'Recommendation from Analysts Recommendation Mean',
             'Recommdation from Analysts Recommendation Key']



st.write("If stock not in options add by input below")
add_tick = st.text_input(label="Add stock, enter ticker")

if add_tick:
    ticker_list.append(add_tick)

global selected_tickers
selected_tickers = st.multiselect(label="Select Stocks TO COMPARE", options=ticker_list)
start_date = st.date_input(label="Start Date FOR PAST PRICES", value=dt.datetime.now().date() - dt.timedelta(weeks=1))
end_date = st.date_input(label="End DATE FOR PAST PRICES")
if start_date >= end_date:
    st.warning("Start Date cannot be after end date, Please change the dates.")
    st.stop()

# print(start_date)
# print(type(start_date))
# print(str(start_date))
selected_all_data = yh.download(selected_tickers, start_date, end_date) if selected_tickers else None
# print(selected_all_data)
# print(len(selected_all_data))
# print(type(selected_all_data))

selected_display_result = st.multiselect(label="What do you want to see?", options=data_opts)

def create_table_from_info_data(field):
    datalist = []
    for ticker in selected_tickers:
        ticker_info = yh.Ticker(ticker)
        try:
            fieldinfo = ticker_info.info[field]
        except KeyError:
            fieldinfo = None
        datalist.append(fieldinfo)
    df = pd.DataFrame(datalist, index=selected_tickers, columns= ["Value"])
    st.table(df)
    return df

# left_col, right_col, rm_col = st.columns([0.2, 0.4, 0.4])

def put_button_and_graph(data, field=None):
    with st.expander(":rainbow[Graph]", icon="💹"):
        st.scatter_chart(data)
        # st.bar_chart(data)

def button_for_binfo(name, info):
    with st.expander(f"What is {name}?", icon="❓"):
        st.markdown(name + " is " + info)

def button_for_minfo(name, info):
    with st.expander(f"How to evaluate {name}", icon="⁉️"):
        st.markdown(info)
        # st.image(image, width=100)

if selected_all_data is not None and selected_display_result is not None:

    st.write("Tabulized data")
    st.table(selected_all_data.head())

    closing_data = selected_all_data['Close']
    st.write("Closing data graph")
    st.line_chart(closing_data)

    if "Forward P/E" in selected_display_result or "Trailing P/E" in selected_display_result:
        st.write("More on P/E")
        button_for_binfo('Price per Earning', "In simple terms, a good P/E ratio is lower than the average P/E ratio, which is between 20–25. When looking at the P/E ratio alone, the lower it is, the better.")
        
        button_for_binfo("Trailing P/E VS. Forward P/E", """The trailing P/E ratio differs from the forward P/E,
                     which uses earnings estimates or forecasts for the next four quarters or next projected 12 months of earnings.
                     As a result, forward P/E can sometimes be more relevant to investors when evaluating a company.
                     Nonetheless, as forward P/E relies on estimated future earnings, it is prone to miscalculation and/or
                     the bias of analysts. Companies may also underestimate or mis-state earnings in order to beat consensus
                     estimate P/E in the next quarterly earnings report.
                     Both ratios are useful during acquisitions.
                     The trailing P/E ratio is an indicator of past performance of the company being acquired.
                     Forward P/E represents the company's guidance for the future.
                     Typically valuations of the acquired company are based on the latter ratio.
                     However, the buyer can use an earnout provision to lower the acquisition price, with the option of making an additional payout if the targeted earnings are achieved.""")
    
    if "Trailing P/E" in selected_display_result:
        st.write("Trailing P/E")
        data = create_table_from_info_data("trailingPE")
        put_button_and_graph(data, "trailingPE")
        button_for_binfo("Trailing P/E",
                     """a relative valuation multiple that is based on the last 12 months of actual earnings.
                       It is calculated by taking the current stock price and dividing it by
                         the trailing earnings per share (EPS) for the past 12 months.""")
        # button_for_minfo("Trailing P/E", "20-25", "https://www.investopedia.com/thmb/hgAHxNw5ETOZQVBlGF7WQH50Pjo=/750x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/Term-Definitions_Trailing-price-to-earnings---RECIRC-blue-009ebaf051bf4d45bb4583bd4d67c12f.jpg")
        # button_for_minfo("Trailing P/E", "20-25")
        # if st.button(":rainbow[Graph]"):
        #     st.line_chart(data)
        #     st.bar_chart(data)
        #     st.scatter_chart(data)
        #     st.area_chart(data)
        #     st.map(data)
        # ltpe = []

        # for ticker in selected_tickers:
        #     ticker_info = yh.Ticker(ticker)
        #     try:
        #         div = ticker_info.info['trailingPE']
        #     except KeyError:
        #         div = None
        #     ltpe.append(div)
        # st.table(pd.DataFrame(ltpe, index=selected_tickers))
    
    if "Forward P/E" in selected_display_result:
        st.write('Forward P/E')
        data = create_table_from_info_data("forwardPE")
        put_button_and_graph(data, "forwardPE")
        button_for_binfo("Future P/E",
                        """a valuation metric that uses earnings forecasts to
                        calculate the ratio of the share price to projected earnings per share.
                        It divides the current share price of a company
                            by the estimated future (“forward”) earnings per share (EPS) of that company.""")

    # if "Forward P/E" in selected_display_result or "Trailing P/E" in selected_display_result:      
    #     button_for_binfo('Price per Earning', "In simple terms, a good P/E ratio is lower than the average P/E ratio, which is between 20–25. When looking at the P/E ratio alone, the lower it is, the better.")
        
    #     button_for_binfo("Trailing P/E VS. Forward P/E", """The trailing P/E ratio differs from the forward P/E,
    #                  which uses earnings estimates or forecasts for the next four quarters or next projected 12 months of earnings.
    #                  As a result, forward P/E can sometimes be more relevant to investors when evaluating a company.
    #                  Nonetheless, as forward P/E relies on estimated future earnings, it is prone to miscalculation and/or
    #                  the bias of analysts. Companies may also underestimate or mis-state earnings in order to beat consensus
    #                  estimate P/E in the next quarterly earnings report.
    #                  Both ratios are useful during acquisitions. The trailing P/E ratio is an indicator of past performance of the company being acquired. Forward P/E represents the company's guidance for the future. Typically valuations of the acquired company are based on the latter ratio. However, the buyer can use an earnout provision to lower the acquisition price, with the option of making an additional payout if the targeted earnings are achieved.""")
    # # lfpe = []
    # for ticker in selected_tickers:
    #     ticker_info = yh.Ticker(ticker)
    #     try:
    #         div = ticker_info.info['forwardPE']
    #     except KeyError:
    #         div = None
    #     lfpe.append(div)
    # st.table(pd.DataFrame(lfpe, index=selected_tickers))

    if "Dividend Rate" in selected_display_result:
        st.write("Dividend Rates")
        data = create_table_from_info_data('dividendRate')
        put_button_and_graph(data, 'dividendRate')
        button_for_binfo("Dividend Rates",
                        """a financial ratio that shows how much a company pays
                        out in dividends each year relative to its stock price.""")
    
    if "Dividend Yield" in selected_display_result:
        st.write("Dividend Yield")
        data = create_table_from_info_data('dividendYield')
        put_button_and_graph(data, 'Dividend Yield')
        button_for_binfo('Dividend Yield', 'the amount of money a company pays shareholders for owning a share of its stock divided by its current stock price.')
        button_for_minfo('Dividend Yield', 'Yields from 2% to 6% are generally considered to be a good dividend yield, but there are plenty of factors to consider when deciding if a stock\'s yield makes it a good investment.')

    # ld = []
    # for ticker in selected_tickers:
    #     ticker_info = yh.Ticker(ticker)
    #     try:
    #         div = ticker_info.info['dividendRate']
    #     except KeyError:
    #         div = None
    #     ld.append(div)
    # st.table(pd.DataFrame(ld, index=selected_tickers))

    if "Beta" in selected_display_result:
        st.write(":rainbow[Beta]")
        data = create_table_from_info_data('beta')
        put_button_and_graph(data, "beta")
        button_for_binfo("Beta", "a measure of volatility of the stock compared to the market as a whole(usually S&P500)")
        button_for_minfo("Beta", " Beta greater than 1.0 suggests that the stock is more volatile than the broader market, and a beta less than 1.0 indicates a stock with lower volatility.")
    
    # lb = []
    # for ticker in selected_tickers:
    #     ticker_info = yh.Ticker(ticker)
    #     try:
    #         div = ticker_info.info['beta']
    #     except KeyError:
    #         div = None
    #     lb.append(div)
    # st.table(pd.DataFrame(lb, index=selected_tickers))

    if "Market Capitalization" in selected_display_result:
        st.write("Market Capitalization")
        data = create_table_from_info_data('marketCap')
        put_button_and_graph(data, "marketCap")
        button_for_binfo("Market Capitalization", 
                        "aka market cap, shows how much a company is worth as determined by the total market value of all outstanding shares")

    # lmc = []
    # for ticker in selected_tickers:
    #     ticker_info = yh.Ticker(ticker)
    #     try:
    #         div = ticker_info.info['marketCap']
    #     except KeyError:
    #         div = None
    #     lmc.append(div)
    # st.table(pd.DataFrame(lmc, index=selected_tickers))
    if "Sector" in selected_display_result:
        st.write("Sector")
        create_table_from_info_data('sector')

    if "Volume" in selected_display_result:
        st.write('volume')
        data = create_table_from_info_data('volume')
        put_button_and_graph(data, 'volume')
        button_for_binfo('Volume', 'an indicator that means the total number of shares that have been bought or sold in a specific period of time or during the trading day.')

    if "Profit Margins" in selected_display_result:
        st.write('Profit Margins')
        data = create_table_from_info_data('profitMargins')
        put_button_and_graph(data, 'Profit Margins')
        button_for_binfo('Profit Margins', 'a common measure of the degree to which a company or a particular business activity makes money.')

    if "Trailing EPS" in selected_display_result:
        st.write('Trailing Eps')
        data = create_table_from_info_data('trailingEps')
        put_button_and_graph(data, 'Trailing EPS')
        button_for_binfo('Trailing EPS', 'is a company\'s earnings generated over a prior period (often a fiscal year) reported on a per-share basis.')

    if "Forward EPS" in selected_display_result:
        st.write('Forward Eps')
        data = create_table_from_info_data('forwardEps')
        put_button_and_graph(data, 'forwardEps')

    if "Peg Ratio" in selected_display_result:
        st.write('Peg Ratio')
        data = create_table_from_info_data('pegRatio')
        put_button_and_graph(data, 'Peg Ratio')
        button_for_binfo("PEG Ratio", 'a company\'s Price/Earnings ratio divided by its earnings growth rate over a period of time (typically the next 1-3 years)')

    if "Ebitda" in selected_display_result:
        st.write('ebitda')
        data = create_table_from_info_data('ebitda')
        put_button_and_graph(data, 'ebitda')
        button_for_binfo('Ebitda','an alternate measure of profitability to net income. By including depreciation and amortization as well as taxes and debt payment costs, EBITDA attempts to represent the cash profit generated by the company\'s operations.')

    if "Total Revenue" in selected_display_result:
        st.write('Total Revenue')
        data = create_table_from_info_data('totalRevenue')
        put_button_and_graph(data, "total revenue")
        button_for_binfo('Total Revenue', 'the total of all sales of products or services before expenses are taken out. It is calculated by multiplying the price of the products or services by the number of units sold.')

    if "Full Time Employees" in selected_display_result:
        st.write("Full Time Employees")
        data = create_table_from_info_data("fullTimeEmployees")
        put_button_and_graph(data, "fullTimeEmployees")
        button_for_binfo('Full Time Employees', 'the number of full time employees at the company.')
        button_for_minfo("Full Time Employees", 'They tell us about the size of the company.')

    if "Year Low" in selected_display_result:
        st.write("Year Low")
        data = create_table_from_info_data('fiftyTwoWeekLow')
        put_button_and_graph(data, "fiftyTwoWeekLow")
        button_for_binfo("Year Low/ Fiftytwo week Low", "the lowest price at which an asset has been traded over the prior 52 weeks")
    
    if "Year High" in selected_display_result:
        st.write("Year High")
        data = create_table_from_info_data('fiftyTwoWeekHigh')
        put_button_and_graph(data, "fiftyTwoWeekHigh")
        button_for_binfo("Year High/ Fiftytwo week High", "the highest price at which an asset has been traded over the prior 52 weeks")

    if "Recommdation from Analysts Recommendation Mean" in selected_display_result:
        st.write("Recommendation from Analysts",'recommendationMean')
        data = create_table_from_info_data('recommendationMean')
        put_button_and_graph(data, 'recommendationMean')
        button_for_binfo("Recommdation from Analysts Recommendation Mean", "It is the Recommendation from Analysts.")

    if "Recommdation from Analysts Recommdation Key" in selected_display_result:
        st.write("Recommdation from Analysts", 'recommendationKey')
        data = create_table_from_info_data('recommendationKey')
        put_button_and_graph(data, 'recommendationKey')
        button_for_binfo("Recommdation from Analysts Recommdation Key", "It is the Recommendation from Analysts, usually word 'buy' or 'sell'.")

    # ls = []
    # for ticker in selected_tickers:
    #     ticker_info = yh.Ticker(ticker)
    #     try:
    #         div = ticker_info.info['sector']
    #     except KeyError:
    #         div = None
    #     ls.append(div)
    # st.table(pd.DataFrame(ls, index=selected_tickers))



    # closing_data_graph = plt.plot(closing_data)
    # st.pyplot(closing_data)

    # st.multiset(label="Select Stocks", options=ticker_list, ":rainbow[options]")

# 'volume'
# 'profitMargins'
# 'trailingEps': 11.52,
#  'forwardEps': 13.3,
# 'pegRatio': 2.37,
# 'ebitda': 125981999104,
# 'totalRevenue': 236583993344,
# 'recommendationMean': 1.7,
#  'recommendationKey': 'buy',
