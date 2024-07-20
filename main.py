import streamlit as st
from streamlit_option_menu import option_menu
import requests  # 不要忘记导入 requests 库
from datetime import datetime, timedelta
import yfinance as yh
import pandas as pd
from investobot8 import ticker
from investobot8 import *
from sqlalchemy import create_engine, Column, String, Integer, DateTime, MetaData


#from sqlalchemy.orm import declarative_base, sessionmaker
import community3
from community3 import Message

ticker=None

# 用户注册
def register_user(username, password):
    response = requests.post('http://localhost:5000/register', json={'username': username, 'password': password})
    return response.json()

# 用户登录
def login_user(username, password):
    response = requests.post('http://localhost:5000/login', json={'username': username, 'password': password})
    if response.status_code == 200:
        st.session_state['logged_in'] = True
    else:
        st.session_state['logged_in'] = False
    return response.json()

# 检查用户是否已登录
def is_logged_in():
    return st.session_state.get('logged_in', False)

# 定义页面名称及对应的 Python 文件
PAGES = {
    "Home": "homepage1.py",
    "Investo-bot": "investobot8.py",
    "Compare Stocks": "dashboard_interactive_with_expanders.py",
    "Profolio": "portfolioexampleandpage.py",
    "Community": "community3.py",
    "Register": "register.py",
    "Login": "login.py"
    
}

# 处理页面导航会话状态
if "selected_tab" not in st.session_state:
    st.session_state.selected_tab = "Home"

# 检查 URL 参数以进行页面导航
query_params = st.query_params
if "tab" in query_params:
    selected_tab = query_params["tab"][0]
    st.session_state.selected_tab = selected_tab
else:
    selected_tab = st.session_state.selected_tab

# 创建顶部导航栏
selected_tab = option_menu(
    menu_title=None,  # required
    options=list(PAGES.keys()),  # required
    icons=["house", "robot", "graph-up-arrow","briefcase","people","person-add", "person"],  # optional icons
    menu_icon="cast",  # optional icon
    default_index=list(PAGES.keys()).index(st.session_state.selected_tab),  # default selected page
    orientation="horizontal",
    key="menu_option"
)

# 更新会话状态
st.session_state.selected_tab = selected_tab

page = PAGES[selected_tab]

# 非缓存版本的页面加载函数
def load_page(page):
    with open(page, "r", encoding="utf-8") as f:
        code = f.read()
    return code

# 动态加载并执行所选页面
@st.cache_data(ttl=1)
def load_page(page):
    with open(page, "r", encoding="utf-8") as f:
        code = f.read()
    return code

# 隔离动态代码执行以避免上下文问题
def run_page_code(code, page_prefix):
    local_vars = {}
    exec(code, globals().copy().update({"PAGE_PREFIX": page_prefix}), local_vars)

page_code = load_page(page)
run_page_code(page_code, page)
