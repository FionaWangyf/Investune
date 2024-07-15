import datetime
import matplotlib.pyplot as plt
import streamlit as st
import pandas_datareader as pdr
import yfinance as yh

def get_recent_data(ticker):
    start_date = datetime.datetime.now() - datetime.timedelta(days=30)
    end_date = str(datetime.datetime.now().date())
    
    # 获取股票数据
    yhoo = yh.download(ticker, start_date, end_date)
    
    # 获取前几行数据作为示例
    data = yhoo.head()
    
    # 仅提取收盘价s
    closing_data = yhoo['Close']
    
    # 绘制收盘价图表
    plt.plot(closing_data)
    plt.title(f"{ticker} Closing Prices")
    plt.xlabel("Date")
    plt.ylabel("Closing Price")
    plt.show()
    
    return closing_data, data


