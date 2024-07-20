from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import streamlit as st

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Initializing SQLAlchemy
db = SQLAlchemy(app)

# Defining the user model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

# creating database
with app.app_context():
    db.create_all()

# 用户注册 User Registration Routing
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # 检查用户名和密码是否为空
    if not username or not password:
        return jsonify({'message': 'Username and password cannot be empty'}), 400
    
    #检查是否已有相同用户名的用户
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 400
    #创建新用户，并将密码哈希化
    new_user = User(username=username, password_hash=generate_password_hash(password))
    db.session.add(new_user)#将新用户添加到数据库
    db.session.commit()#提交更改           

    return jsonify({'message': 'User registered successfully'})

# 用户登录
@app.route('/login', methods=['POST'])
def login():
    #从请求中获取数据
    data = request.json
    username = data.get('username')
    password = data.get('password')
    #检查用户是否存在，并检查密码是否正确
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        #st.session_state.selected_tab = "Home"
        #st.rerun()
        return jsonify({'message': 'Login successful'}),200
    return jsonify({'message': 'Invalid credentials'}), 400

if __name__ == '__main__':
    app.run(port=5000)
