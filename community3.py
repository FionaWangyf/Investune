import streamlit as st
import time
from datetime import datetime
import pytz
from sqlalchemy import create_engine, Column, String, Integer, DateTime, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker

# 初始化数据库连接
DATABASE_URL = "sqlite:///community_chat.db"
engine = create_engine(DATABASE_URL)
metadata = MetaData()
Base = declarative_base()

# 定义消息表模型
class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    message = Column(String, nullable=False)
    time = Column(DateTime, nullable=False)

# 创建表（如果不存在）
Base.metadata.create_all(engine)

# 创建数据库会话
global Session
Session = sessionmaker(bind=engine)
global session
session = Session()

# 定义北京时区
beijing_tz = pytz.timezone('Asia/Shanghai')

st.header("Investune Users Community")
st.subheader("Post your updates on in!")

# 获取已有的消息
def get_messages():
    return session.query(Message).all()

# 显示已有消息
for message in get_messages():
    st.write(f""":rainbow[*{message.username}*] ({message.time.astimezone(beijing_tz).strftime('%Y-%m-%d %H:%M:%S')})  
                 {message.message}""")

# 输入新消息
username = st.text_input("Enter your name:")

if username:
    prompt = st.chat_input("Write a stock message to the community:")
    if prompt:
        with st.chat_message("assistant",avatar="🙏"):
            st.write(f"Dear {username}, thank you for adding your post to our community! We hope you get benefited from posts here as well!")

        # 将消息存储到数据库
        now_beijing = datetime.now(beijing_tz)
        new_message = Message(username=username, message=prompt, time=now_beijing)
        session.add(new_message)
        session.commit()

        time.sleep(3)
        st.rerun()
