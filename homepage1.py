import streamlit as st
import yfinance as yh
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# 自定义 CSS 样式
st.markdown(
    """
    <style>
    .title {
        font-size: 50px;
        color: #DB7093;
        text-align: center;
        margin-top: 50px;
    }
    .subtitle {
        font-size: 25px;
        color: #FF6347;
        text-align: center;
        margin-top: 20px;
    }
    .description {
        font-size: 18px;
        color: #40E0D0;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 50px;
    }
    .centered-button-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 30px;
    }
    .centered-button {
        padding: 10px 20px;
        font-size: 16px;
        color: #fff;
        background-color: #007BFF;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    .centered-button:hover {
        background-color: #0056b3;
    }
    .login-button {
        position: absolute;
        top: 10px;
        right: 10px;
    }
    body {
        background-color: #f0f2f6;
    }
    .index-card {
        display: inline-block;
        width: 200px;
        margin: 10px;
        padding: 20px;
        border: 1px solid #ddd;
        border-radius: 8px;
        text-align: center;
        background-color: #fff;
    }
    .index-title {
        font-size: 18px;
        font-weight: bold;
        color: #1e90ff;
    }
    .index-value {
        font-size: 24px;
        font-weight: bold;
    }
    .index-change {
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 添加图片
st.image("./logo.png", width=100)

# 页面标题和副标题
st.markdown("<h1 class='title'>Welcome to Investune</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='subtitle'>Your Personal Investment Assistant</h2>", unsafe_allow_html=True)

# 描述
st.markdown(
    "<p class='description'>Investune helps you analyze stocks and make informed investment decisions. "
    "Use the top menu to navigate to the Chatbot for stock analysis or the Dashboard for comparing different stocks.</p>",
    unsafe_allow_html=True
)

# 添加居中的按钮
st.markdown('<div class="centered-button-container">', unsafe_allow_html=True)
button_clicked = st.button('Get Started', key='get_started')
st.markdown('</div>', unsafe_allow_html=True)

if button_clicked:
    if st.session_state.get('logged_in', False):
        st.session_state.selected_tab = "Investo-bot"
    else:
        st.session_state.selected_tab = "Login"
    st.experimental_rerun()

# 获取最近1年的数据的函数
def get_recent_data(ticker):
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=365)
    
    # 使用 yh.download 获取股票数据
    yhoo = yh.download(ticker, start=start_date, end=end_date)
    
    # 仅提取收盘价
    closing_data = yhoo['Close']
    
    return closing_data

# 指数基金的股票代码和名称
index_funds = {
    '^GSPC': 'S&P 500',
    '^DJI': 'Dow',
    '^IXIC': 'Nasdaq',
    'BTC-USD': 'Bitcoin',
    'GC=F': 'Gold',
    '^N225': 'Nikkei 225',
    '^HSI': 'Hang Seng Index',
    '^TNX': '10-Year Treasury Yield',
    '^KLSE': 'FTSE Bursa Malaysia KLCI',
    '^CMC200':'CMC Crypto 200 Index by Solacti '

}

# 准备图表显示
num_funds = len(index_funds)
rows = (num_funds + 3) // 4  # 计算行数，每行显示4个图表

# 创建 plotly 图表
fig = make_subplots(rows=rows, cols=4, subplot_titles=list(index_funds.values()))

# 循环处理每个指数基金
for i, (ticker, name) in enumerate(index_funds.items()):
    close_prices = get_recent_data(ticker)
    row = i // 4 + 1
    col = i % 4 + 1
    fig.add_trace(go.Scatter(x=close_prices.index, y=close_prices, mode='lines', name=name), row=row, col=col)

# 更新布局
fig.update_layout(height=250 * rows, width=1200, showlegend=False, title_text="Index Fund Closing Prices")
st.markdown("<h2 class='subtitle'>Popular 10 Index Funds </h2>", unsafe_allow_html=True)

# 显示图表
st.plotly_chart(fig)

# 添加更多内容
st.markdown(
    """
    <div style="text-align: center; margin-top: 50px;">
        <p>Provided by Sia Aggarwal, Wang Yufan, Wang Xuanhao and Xia Yuting.</p>
    </div>
    """,
    unsafe_allow_html=True
)
