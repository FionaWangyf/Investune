# homepage.py
import streamlit as st

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
    body {
        background-color: #f0f2f6;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 添加图片
st.image("./logo.png", width=200, caption="Investo-Bot Logo")

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
if st.button('Get Started'):
    st.session_state.selected_tab = "Chatbot"
    st.rerun()

# 添加更多内容
st.markdown(
    """
    <div style="text-align: center; margin-top: 50px;">
        <p>Provided by Sia Aggarwal, Wang Yufan, Wang Xuanhao and Xia Yuting.</p>
    </div>
    """,
    unsafe_allow_html=True
)
