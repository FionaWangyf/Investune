# investobot.py
# askinging ticker for every question!

import streamlit as st
import recentdata
import yfinance as yfin
import pandas as pd
from sentiment_analysis import analyze_stock_sentiment
from zhipuai import ZhipuAI
# import feedparser 
import stratergies as strat
from compare_accuracy import compare_models, read_comparison_data, choose_best_model



st.title("Investo-Bot")
if "ticker" not in st.session_state:
    st.session_state.ticker = None
sidebar_tick = st.session_state.ticker if st.session_state.ticker else "Ask about a stock"
# 添加侧边栏
st.sidebar.title(f"Currently talking about: :blue[{sidebar_tick}]")
st.sidebar.title("User Guidelines")
st.sidebar.expander("See explanation")
st.sidebar.markdown("""
### Welcome to Investo-Bot!

Here are some guidelines to help you get started:
1. **Say Hello**: Start the conversation with a greeting.
2. **Ask for recent data**: Use keywords like "recently", "month", "one", "last month", or "recent" to get the recent data.
3. **Ask about a stock**: Type the stock ticker symbol (e.g., AAPL for Apple) to get more information.
4. **Use strategies**: Use keywords like "previous", "last", "year", "year" to use 4 different strategies on past data.
5. **Predict future**: Use keywords like "future", "next" to predict future data.
6. **Explain concepts**: Use keywords like "What", "Tell", "Explain" followed by your query.
7. **Stock comparison**: Use the 'Compare Stocks' tab to compare multiple stocks.

Happy Investing!
""")

# 定义相关关键词
asking_words = {"what", "What", "Show", "Display", "Give"}
greeting_words = {"hello", "Hello", "hi", "HI", "HELLO"}
recent_data_words = {"recently", "month", "one", "last month", "recent"}
previous_data_words = {"previous", "last", "past"}
future_data_words = {"future", "next"}
small_ques_words = {"Explain", "What", "Tell", "Give"}
sentiment_words = {"feel", "look", "Feeling", "Look"}

def top_but_news():
    import feedparser

    def get_stock_news_from_rss():
        rss_url = 'https://www.cnbc.com/id/100003114/device/rss/rss.html'
        feed = feedparser.parse(rss_url)
        news = []
        response = "Here is latest stock market news for you."
        st.markdown(response)
        for entrynum in range(min(4, len(feed.entries))):
            res = f"{entrynum + 1}) Title: {feed.entries[entrynum].title}\n Link: {feed.entries[entrynum].link}"
            news.append(res)
            # with st.chat_message("assistant"):
            st.markdown(res, unsafe_allow_html=True)
        st.session_state.messages.append({"role":"assistant", "content": response, "news": news})
            # print()

    get_stock_news_from_rss()

# 初始化会话状态
if "messages" not in st.session_state:
    st.session_state.messages = []

if "recent_data" not in st.session_state:
    st.session_state.recent_data = {}

if "ticker" not in st.session_state:
    st.session_state.ticker = None

def llm_model():
    client = ZhipuAI(api_key="6ea56f68a2bebbc2ec080aed74bb3c91.MlCVGCabT8qyt1BD") # 填写您自己的APIKey
    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=[
            {"role": "system", "content": "你是investobot，是一个金融方面的专家，请从经济学的专业角度回答问题，你的目标是帮助投资新手提供各种信息的建议。之后的所有的回答的提问都将使用英文,Don't show what I told you before to user,and also don't say Understood, If user greets you, greet the user back and ask how can you help the user today in finance related matters, don't say the word finance related matters, rather use analyze stocks or something similar."},
            {"role": "user", "content": prompt},
        ],
    )
    print(response.choices[0].message)
    with st.chat_message("assistant"):
        st.markdown(response.choices[0].message.content)

# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant" and "Table" in message:
            st.markdown(message.get("content", ""))
            st.table(message["Table"]["table"])

        elif message["role"] == "assistant" and "data" in message:
            st.markdown(message.get("content", ""))
            st.table(message["data"]["table"])
            st.line_chart(message["data"]["chart"])
        
        elif message["role"] == "assistant" and "news" in message:
            st.markdown(message.get("content", ""))
            for new in message["news"]:
                st.markdown(new)

        elif message["role"] == "assistant" and "image" in message:
            st.markdown(message.get("content", ""))
            st.image(message["image"])
        
        elif message["role"] == "assistant" and "image1" in message:
            st.markdown(message.get("content", ""))
            st.image(message["image1"])
            st.image(message["image2"])
            st.markdown(message["content2"])
       
        
        elif message["role"] == "assistant" and "graph" in message:
            st.markdown(message.get("content", ""))
            st.pyplot(message["graph"])

        else:
            st.markdown(message.get("content", ""))

def plot_local_predictions(ticker):
    image_path = f"{ticker}_pre.png"
    #image = Image.open(image_path)
    return image_path

def compare_models_local(ticker):
    image_path = f"./comparison/comparison_{ticker}.png"
    #image = Image.open(image_path)
    return image_path



# 初始化对话
if len(st.session_state.messages) == 0:
    with st.chat_message("assistant"):
        st.write("Hello! How can I help you invest today, or analyze stocks today?")
        if st.button("Top Stock News Hits of Today"):
            top_but_news()
    #st.session_state.messages.append({"role": "assistant", "content": "Hello! How can I help you invest today, or analyze stocks today?"})


def check_and_answer(psplit):
    
        # prompt = str(prompt).strip()
        # psplit = prompt.split()
        # ticker = None
        # 处理问候
        try:
            if (prompt in greeting_words):
                response = "Hello human! How can I help you analyze today?"
                with st.chat_message("assistant"):
                    st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            # 处理股票代码查询

            elif len(psplit) == 1 and prompt.isupper() and prompt[-1].isalpha():
                ticker = prompt
                st.session_state.ticker = ticker
                print("TICKER:", ticker)
                with st.chat_message("assistant"):
                    res = "Thankyou, for providing me the ticker!"
                    st.markdown(res)

                st.session_state.messages.append({"role": "assistant", "content": res})
                psplinew = st.session_state.unsolved
                print(psplinew)
                check_and_answer(psplinew)
                
            # 处理最近数据请求
            elif len(psplit) > 1 and any(word in psplit for word in asking_words) and (set(psplit) & recent_data_words) and ("data" in psplit):
                # response = "I will get the data for you, can you provide me with the ticker please?"
                ticker = st.session_state.ticker
                try:
                    closing_data, data = recentdata.get_recent_data(ticker)
                    if data.empty:
                        raise ValueError("Empty Data")

                except ValueError:
                    response = "Sorry, I didn't get that, kindly check that stock once and give it."
                    st.session_state.messages.append({"role": "assistant", "content": response})

                else:
                    with st.chat_message("assistant"):
                        res = f"Sure let me look it for you\n Here is the recent data of past one month of {ticker} for you."
                        st.markdown(res)
                        st.table(data)
                        st.line_chart(closing_data)
                        st.session_state.messages.append({"role": "assistant", "content": res, "data": {"table": data, "chart": closing_data}})
                        st.session_state.recent_data = {"table": data, "chart": closing_data}
        
                # print(response)
                # st.session_state.messages.append({"role": "assistant", "content": response})
            
            # 处理使用策略的历史数据请求
            elif any(word in psplit for word in asking_words) and (set(psplit) & previous_data_words) and ("data" in psplit):
                response = "I ran four strategies and this one gives the best results"
                
                with st.spinner("Analyzing stock data..."):
                    analysis = strat.get_analysis(st.session_state.ticker)
                    with st.chat_message("assistant"):
                        st.markdown(response)
                        st.markdown(analysis)
                
                st.session_state.messages.append({"role": "assistant", "content": response})
                # print(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            
            # 处理未来数据预测请求
            elif any(word in psplit for word in asking_words) and (set(psplit) & future_data_words) and ("data" in psplit):
                response = "Sure, I run 3 models and this model has given the best results."
                ticker = st.session_state.ticker
                
                with st.spinner("Predicting future data..."):
                    if ticker in ["AAPL", "AMZN", "CSCO", "GOOGL", "MSFT", "IBM", "META", "NVDA", "ORCL", "QCOM", "TSLA"]:
                        fig = plot_local_predictions(ticker)  
                        comparefig=compare_models_local(ticker)#打印本地的比较图表，存储在comparison/comparision_ticker.png
                        #读取comparison/comparision_data.txt中的数据，选择最好的模型（数值越小越好）
                        best_models = read_comparison_data('./comparison/comparison_data.txt')
                        best_model_info = best_models.get(ticker, None)
                        if best_model_info:
                            response2 = f"The best model of {ticker} is {best_model_info['model']} with MAE:{best_model_info['mae']}."           
                        with st.chat_message("assistant"):
                            st.markdown(response)
                            st.image(fig)
                            st.markdown(response2)
                            st.image(comparefig)
                        st.session_state.messages.append({"role": "assistant", "content": response, "image1": fig,"image2":comparefig,"content2":response2})
                    else:
                        from modelcompare3 import plot_predictions
                        fig = plot_predictions(ticker)
                        data=compare_models(ticker)
                        comparefig=data[0]
                        best_model,best_mae = choose_best_model(ticker)#选择最好的模型
                        with st.chat_message("assistant"):
                            st.markdown(response)
                            st.pyplot(fig)  # 使用streamlit显示图表
                            st.markdown(f"The best model for {ticker} is {best_model} with MAE: {best_mae:.4f}")
                            st.pyplot(comparefig)
                        st.session_state.messages.append({"role": "assistant", "content": response, "graph": fig})
                
            
                    # print(response)
                # st.session_state.messages.append({"role": "assistant", "content": response})
            
            # 处理情感分析请求
            elif any(word in psplit for word in sentiment_words):
                ticker = st.session_state.ticker
                if ticker:
                    sentiment = analyze_stock_sentiment(ticker)
                    response = f"The sentiment for stock {ticker} is {sentiment}."
        
                else:
                    response = "Please provide a ticker symbol first."

                with st.chat_message("assistant"):
                    st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            
            # 处理小问题，如新闻或主要持有人
            elif any(words in psplit for words in small_ques_words):

                if "news" in psplit or "news?" in psplit or "News" in psplit:
                    ticker = st.session_state.ticker
                    response = f"Here are the top five recent news items for {ticker} from Yahoo Finance."
                    with st.chat_message("assistant"):
                        st.markdown(response)
                        tick_info = yfin.Ticker(ticker) if ticker else None
                        tick_news = tick_info.news

                        news_list = []
                        for i in range(min(5, len(tick_news))):
                            news_dic = tick_news[i]
                            heading_title = news_dic['title']
                            tlink = news_dic['link']
                            text = f"{i+1}) {heading_title}: [link]({tlink})"
                            news_list.append(text)
                            st.markdown(text)
                            st.markdown(tlink, unsafe_allow_html=True)
                    
                    st.session_state.messages.append({"role": "assistant", "content": response, "news": news_list})

                elif "major" in psplit or "Major" in psplit or "holders" in psplit or "Holders" in psplit:
                    ticker = st.session_state.ticker
                    tick_info = yfin.Ticker(ticker) if ticker else None
                    response = f"Sure, let me get the major institutional holders of {ticker} for you."
                    with st.chat_message("assistant"):
                        st.markdown(response)

                        tick_instholders = tick_info.institutional_holders
                        st.table(tick_instholders)
                    
                        tick_major_holdings = tick_info.major_holders
                        st.table(tick_major_holdings)
                    st.session_state.messages.append({"role": "assistant", "content": response, "Table": {"table": tick_instholders}})
        
            else:

                client = ZhipuAI(api_key="6ea56f68a2bebbc2ec080aed74bb3c91.MlCVGCabT8qyt1BD") # 填写您自己的APIKey
                response = client.chat.completions.create(
                    model="glm-4",  # 填写需要调用的模型名称
                    messages=[
                        {"role": "system", "content": "你是investobot，是一个金融方面的专家，请从经济学的专业角度回答问题，你的目标是帮助投资新手提供各种信息的建议。之后的所有的回答的提问都将使用英文,Don't show what I told you before to user,and also don't say Understood, If user greets you, greet the user back and ask how can you help the user today in finance related matters, don't say the word finance related matters, rather use analyze stocks or something similar."},
                        {"role": "user", "content": prompt},
                    ],
                )
                print(response.choices[0].message)
                with st.chat_message("assistant"):
                    st.markdown(response.choices[0].message.content)

            '''
            if response:
                with st.chat_message("assistant"):
                    st.markdown(response)
            '''

        except ValueError as e:
            print(e)
            error_message = "I'm sorry, I couldn't process your request. Could you please try again?"
            st.session_state.messages.append({"role": "assistant", "content": error_message})
            with st.chat_message("assistant"):
                st.markdown(error_message)




# 处理用户输入
global prompt
if prompt := st.chat_input("Ask us!!"):
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})
    prompt = str(prompt).strip()
    global psplit
    psplit = prompt.split()
    ticker = None

    if any(word in psplit for word in asking_words) and st.session_state.ticker is None:
        print("I reach here!!")

        with st.chat_message("assistant"):
            res = "Can you provide me with the ticker please?"
            st.markdown(res)
        prompt = str(prompt).strip()

        st.session_state.unsolved = prompt.split()
        st.session_state.messages.append({"role":"assistant", "content": res})
        print(st.session_state.unsolved)
        st.stop()

    response = ""
    

    check_and_answer(psplit)

