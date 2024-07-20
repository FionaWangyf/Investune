import streamlit as st
import yhinance as yh
import pandas as pd
from datetime import datetime, timedelta


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
    .centered-button {
        display: flex;
        justify-content: center;
        margin-top: 30px;
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


# 获取最近1年的数据
def get_recent_data(ticker):
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=1825)
    
    # 使用 yh.download 获取股票数据
    yhoo = yh.download(ticker, start=start_date, end=end_date)
    
    # 仅提取收盘价
    closing_data = yhoo['Close'].tolist()
    
    return closing_data

# 指数基金的股票代码和名称
index_funds = {
    '^GSPC': 'S&P 500',
    '^DJI': 'Dow',
    '^IXIC': 'Nasdaq',
    #'BTC-USD': 'Bitcoin',
    '^IXIC':'Nasdaq',
    'GC=F': 'Gold',
    '^N225': 'Nikkei 225',
    '^HSI': 'Hang Seng Index',
    '^TNX': '10-Year Treasury Yield',
    '^KLSE': 'FTSE Bursa Malaysia KLCI'
}

# 生成指数基金数据
data = []
for ticker, name in index_funds.items():
    close_prices = get_recent_data(ticker)
    data.append({
        "name": name,
        "url": f"https://finance.yahoo.com/quote/{ticker}",
        "views_history": close_prices
    })

# 创建DataFrame
df = pd.DataFrame(data)

# 确定 y_max 值，避免空序列错误
max_value = max([max(x) for x in df['views_history'] if x], default=1000)



# 页面标题和副标题
st.markdown("<h1 class='title'>Welcome to Investo-Bot</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='subtitle'>Your Personal Investment Assistant</h2>", unsafe_allow_html=True)

# 描述
st.markdown(
    "<p class='description'>Investo-Bot helps you analyze stocks and make informed investment decisions. "
    "Use the top menu to navigate to the Chatbot for stock analysis or the Dashboard for comparing different stocks.</p>",
    unsafe_allow_html=True
)

# 添加按钮
if st.button('Get Started', key='get_started'):
    if st.session_state.get('logged_in', False):
        st.session_state.selected_tab = "Chatbot"
    else:
        st.session_state.selected_tab = "Login"
    st.experimental_rerun()

st.markdown("<h2 class='subtitle'>Index Funds</h2>", unsafe_allow_html=True)

# 使用Streamlit显示表格
st.dataframe(
    df,
    column_config={
        "name": "Index Fund Name",
        "url": st.column_config.LinkColumn("Fund URL"),
        "views_history": st.column_config.LineChartColumn(
            "Closing Prices (past 5 year)", y_min=0, y_max=max(max_value, 1000)
        ),
    },
    hide_index=True,
)


# 添加更多内容
st.markdown(
    """
    <div style="text-align: center; margin-top: 50px;">
        <p>Provided by Sia Aggarwal, Wang Yufan, Wang Xuanhao and Xia Yuting.</p>
    </div>
    """,
    unsafe_allow_html=True
)
