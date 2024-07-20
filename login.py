import streamlit as st
import requests

# 用户登录
def login_user(username, password):
    response = requests.post('http://localhost:5000/login', json={'username': username, 'password': password})
    if response.status_code == 200:
        st.session_state['logged_in'] = True
    else:
        st.session_state['logged_in'] = False
    return response.json()

st.title('Login')

login_username = st.text_input('Username')
login_password = st.text_input('Password', type='password')
if st.button('Login'):
    result = login_user(login_username, login_password)
    st.write(result)
    if st.session_state['logged_in']:
        st.session_state.selected_tab = "Home"
        st.rerun()

st.markdown("<hr>", unsafe_allow_html=True)
if st.button('Register'):
    st.session_state.selected_tab = "Register"
    st.rerun()
