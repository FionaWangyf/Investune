import streamlit as st
import requests

# 用户注册
def register_user(username, password):
    response = requests.post('http://localhost:5000/register', json={'username': username, 'password': password})
    return response.json()

st.title('Register')

register_username = st.text_input('Username')
register_password = st.text_input('Password', type='password')
if st.button('Register'):
    result = register_user(register_username, register_password)
    st.write(result)
    if result.get('message') == 'User registered successfully':
        st.session_state.selected_tab = "Login"
        st.rerun()
