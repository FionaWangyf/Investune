# main.py
import streamlit as st
from streamlit_option_menu import option_menu

# 定义页面名称和对应的 Python 文件
PAGES = {
    "Home": "homepage.py",
    "Chatbot": "investobot1.py",
    "Compare Stocks": "dashboard_interactive_with_expanders.py"
}

# 处理页面跳转的会话状态
if "selected_tab" not in st.session_state:
    st.session_state.selected_tab = "Home"

# 创建顶端导航栏
selected_tab = option_menu(
    menu_title=None,  # required
    options=list(PAGES.keys()),  # required
    icons=["house", "robot", "graph-up-arrow"],  # 可选图标
    menu_icon="cast",  # 可选图标
    default_index=list(PAGES.keys()).index(st.session_state.selected_tab),  # 默认选中的页面
    orientation="horizontal",
)

# 更新会话状态
st.session_state.selected_tab = selected_tab

page = PAGES[selected_tab]

# 动态加载和执行选中的页面
@st.cache_data(ttl=1)
def load_page(page):
    with open(page, "r", encoding="utf-8") as f:
        code = f.read()
    return code

exec(load_page(page))
