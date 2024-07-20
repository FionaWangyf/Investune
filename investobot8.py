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


global ticker
ticker=None


st.title("Investo-Bot")
if "ticker" not in st.session_state:
    st.session_state.ticker = None
sidebar_tick = st.session_state.ticker if st.session_state.ticker else "Ask about a stock"
# 添加侧边栏
st.sidebar.title(f"Currently talking about: :blue[{sidebar_tick}]")
st.sidebar.title("User Guidelines")
st.sidebar.expander("See explanation")
st.sidebar.markdown("### Welcome to Investo-Bot!")

with st.sidebar.expander("1. Say Hello"):
    st.markdown("""
    Start the conversation with a greeting like "Hello" or "Hi".
    Example: "Hello Investo-Bot!” Or “Hello"
    """)

with st.sidebar.expander("2. Ask for Recent Data"):
    st.markdown("""
    Use keywords like "recently", "month", "one", "last month", or "recent" along with "data" to get the recent data.
    Example: "Show me the recent data of AAPL"
    Note: Make sure to provide the stock ticker symbol first if you haven't already.
    """)

with st.sidebar.expander("3. Ask About a Stock"):
    st.markdown("""
    Provide the stock ticker symbol (e.g., AAPL for Apple) to get more information.
    Example: "AAPL"
    """)

with st.sidebar.expander("4. Use Strategies"):
    st.markdown("""
    Use keywords like "strategy", "best", "profit", "returns", "Sharpe", "Volatility", "risk", "least", "less" along with the word "strategy" to get backtested strategies.
    To get the best strategy for profits, use words like “best” or “max” and “profit” or “returns”.
    To get the highest Sharpe ratio, ask “strategy” and use words like “Sharpe ratio.
    To get the least risk, use words like “less”, “Volatility”, “risky.
    Lastly, to get a full analysis, use words like “deep”, “full”, “strategy” analysis.
    Example: "Which is the best strategy for AMZN with highest returns ?”
    """)

with st.sidebar.expander("5. Predict Future Data"):
    st.markdown("""
    Use keywords like "future", "next", along with "data" to predict future data.
    To get a ML model comparison and also their accuracy.
    Example: "Predict the future data for MSFT”
    """)

with st.sidebar.expander("6. Why use Concepts"):
    st.markdown("""
    Use keywords like "Why" followed by your query to get the reason for financial concepts.
    Example: “Why use growth rate ?” or “Why do we use major holders for stock analysis ?"
    The bot can explain the importance of growth rates, stock market influences, and more.
    """)

with st.sidebar.expander("7. Stock News and Major Holders"):
    st.markdown("""
    Use keywords like "news", "holders", "major holders" to get recent news or major institutional holders of the stock.
    Example: "Give me the news for GOOGL"
    Example: "Who are the major holders of NVDA ?"
    """)

with st.sidebar.expander("8. Sentiment Analysis"):
    st.markdown("""
    Use keywords like "feel", "look", "feeling" to get sentiment analysis of the stock.
    Example: "What is the sentiment for TSLA?”
    """)

with st.sidebar.expander("9. Recommendations"):
    st.markdown("""
    Use keywords like "recommend", "stocks" to get stock recommendations based on historical performance.
    Example: "Can you recommend some stocks?”
    """)

with st.sidebar.expander("10. Getting Started"):
    st.markdown("""
    If you're new to investing, you can ask for beginner-friendly guidance.
    Example: "I'm new to investing, how do I start?"
    """)

with st.sidebar.expander("11. Help and Analysis"):
    st.markdown("""
    If you need help understanding how to analyze stocks or need detailed instructions, ask for assistance.
    Example: “I need help for stock analysis.”
    """)

with st.sidebar.expander("12. How to start"):
    st.markdown("""
    If you don't kwnow how to start investing, ask for suggestions.
    Example: "How can I start investing ?"
    """)


with st.sidebar.expander("13. What Else"):
    st.markdown("""
    If you're unsure of what to do next, ask for suggestions.
    Example: "What else can I do?"
    """)

st.sidebar.markdown("### Examples")

with st.sidebar.expander("General Greetings"):
    st.markdown("""
    - "Hello Investo-Bot!"
    - "Hi"
    """)

with st.sidebar.expander("Recent Data Requests"):
    st.markdown("""
    - "Show me the recent data of AAPL"
    - "What is the recent data for TSLA?"
    """)

with st.sidebar.expander("Stock Information"):
    st.markdown("""
    - "AAPL"
    - "MSFT"
    """)

with st.sidebar.expander("Strategies"):
    st.markdown("""
    - "What is the best strategy for AMZN for max profit?"
    - "Show the strategy with the highest Sharpe ratio for AAPL"
    - "Give me the strategy with the least risk for MSFT"
    - "Give me the strategy full analysis for GOOGL"
    """)

with st.sidebar.expander("Future Predictions"):
    st.markdown("""
    - "Predict the future data for MSFT"
    - "What are the future data predictions for NVDA?"
    """)

with st.sidebar.expander("Concept Explanations"):
    st.markdown("""
    - "Explain growth rate"
    - "What is the importance of stock news?"
    - "Tell me about major holders"
    """)

with st.sidebar.expander("Stock News and Holders"):
    st.markdown("""
    - "Give me the news for GOOGL"
    - "What are the major holders of NVDA?"
    """)

with st.sidebar.expander("Sentiment Analysis"):
    st.markdown("""
    - "What is the sentiment for TSLA?"
    - "How do people feel about AAPL?"
    """)

with st.sidebar.expander("Recommendations"):
    st.markdown("""
    - "Can you recommend some stocks?"
    - "What stocks are recommended for beginners?"
    """)

with st.sidebar.expander("Getting Started"):
    st.markdown("""
    - "I'm new to investing, how do I start investing ?"
    - "Where should I begin with trading?"
    """)

with st.sidebar.expander("Help and Analysis"):
    st.markdown("""
    - "Help me analyze AAPL"
    - "How do I start investing?"
    """)

with st.sidebar.expander("What Else"):
    st.markdown("""
    - "What else can I do?"
    - "What should I do next?"
    """)

st.sidebar.markdown("Happy Investing!")


# 定义相关关键词
asking_words = {"what", "What", "Show", "Display", "Give","Which","which","Can","can"}
greeting_words = {"hello", "Hello", "hi", "HI", "HELLO"}
recent_data_words = {"recently", "month", "one", "last month", "recent"}
previous_data_words = {"previous", "last", "past"}
future_data_words = {"future", "next"}
small_ques_words = {"Explain", "What", "Tell", "Give"}
sentiment_words = {"feel", "look", "Feeling", "Look"}
stratergy_words = {"strategy", "Strategy", "strategies", "Strategies"}
begin_words = {"beginner", "dont", "Don't", "don't", "start", "Dont", "begin", "Begin"}
help_words = {"help", "analyze"}
start_investing = {"start", "invest", "investing", "trading", "Trading", "Invest"}
what_else_words = {"done", "now", "else"}
recommend_words = {"recommend", "stocks", "Recommend", "recommendations", "Recommendations", "Recommendation", "recommendation"}
growth_rate_words = {"growth", "rate", "Growth", "Rate", "growth-rate", "Growth-rate", "Growth-Rate"}
bestst_words = {"best", "profit", "return", "Best", "Profit", "Returns", "Return", "returns"}
maxst_words = {"max", "MAX", "Max"}
riskst_words = {"least", "less", "risk", "volatile", "Volatility", "Least", "risky"}
fullst_words = {"full", "all", "Full", "All","complete", "Complete", "deep", "Deep"}
# till here

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

if "strat_data" not in st.session_state:
    st.session_state.strat_data = None

if "ticker" not in st.session_state:
    st.session_state.ticker = None


def llm_model(prompt):
    with st.spinner("Getting response for you..."):
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
    st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})

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
       
        elif message["role"] == "assistant" and "graph_list" in message:
            st.markdown(message.get("content", ""))
            for line in message["analysis"]:
                st.markdown(line)
            for g in message["graph_list"]:
                st.pyplot(g)
        
        elif message["role"] == "assistant" and "analysis" in message:
            st.markdown(message.get("content", ""))
            st.markdown(message["analysis"])
        
        


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

def stock_recommendations():
    response = "Here are some blue chips stocks which I recommend looking at their last 5 year growth rates."
    data = {
        'Company': ['Apple Inc.', 'Microsoft Corporation', 'Amazon.com, Inc.', 'Alphabet Inc.', 'Meta Platforms, Inc.'],
        'Symbol': ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META'],
        'Last 5 Year Growth Rate (%)': [361.26, 240.90, 90.03, 215.94, 130.57]
    }
    # Create DataFrame
    df = pd.DataFrame(data)
   
    st.markdown(response)
    st.table(df)
    # st.session_state.messages.append({"role":"assistant", "content": response, "Table": df})

# 初始化对话
if len(st.session_state.messages) == 0:
    with st.chat_message("assistant"):
        st.write("Hello! How can I help you invest today, or analyze stocks today?")
        if st.button("Top Stock News Hits of Today"):
            top_but_news()
        if st.button("Get Started with Stock Recommendations"):
            stock_recommendations()
            
    #st.session_state.messages.append({"role": "assistant", "content": "Hello! How can I help you invest today, or analyze stocks today?"})


def check_and_answer(psplit):
        response = None
        prompt = " ".join(psplit)
        # prompt = str(prompt).strip()
        # psplit = prompt.split()
        # ticker = None
        # 处理问候
        try:
            
            if (set(psplit) & greeting_words):
                response = "Hello human! How can I help you analyze today?"
                with st.chat_message("assistant"):
                    st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            
            elif (set(psplit) & what_else_words):
                res = """I see, now that you feel you have done a deep analysis of this stock with me,
                you might see for another stocks and have analysis for them as well,  
                then you add compare these stocks against each other and look for details in the comparing stocks,
                and then if you find all of them are doing great, try simulating your portfolio and optimize it, with our portfolio optimizer."""
                with st.chat_message("assistant"):
                    st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
            
            elif (set(psplit) & recommend_words):
                response = "Here are some blue chips stocks which I recommend looking at their last 5 year growth rates."
                data = {
                    'Company': ['Apple Inc.', 'Microsoft Corporation', 'Amazon.com, Inc.', 'Alphabet Inc.', 'Meta Platforms, Inc.'],
                    'Symbol': ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META'],
                    'Last 5 Year Growth Rate (%)': [361.26, 240.90, 90.03, 215.94, 130.57]
                }
                # Create DataFrame
                df = pd.DataFrame(data)
                with st.chat_message("assistant"):
                    st.markdown(response)
                    st.table(df)
                #st.session_state.messages.append({"role":"assistant", "content": response, "Table": df})
            
            elif (("stocks" in psplit or "stock" in psplit or "Stock" in psplit or "Stocks" in psplit) and 
                  ((set(psplit) & start_investing) or (set(psplit) & begin_words))):
                res = """Don't worry! I can help you get started with stock market, That's what I'm built for!  
                I can provide you a full analysis of a stock just provide me the ticker.
                Try asking these questions below:  
                Give me stock recommendations.
                What is the recent data of AAPL ?  
                What is the best strategy for AAPL for maximum profit ?  
                What is the future data of AAPL ?  
                And maybe you can ask me about the latest news of AAPL, and also the major holders.  
                I can help you with all of these and much more look for user guidelines on your left for more details, just ask me!  
                """
                with st.chat_message("assistant"):
                    st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
        
            elif (set(psplit) & start_investing):
                res = """Surely! I'm here to help you with that!  
                I need you think about two questions:  
                How much risk are you willing to take for a certain amount of investment,  
                and how much profit(range) you are thinking to be returned.
                It's commonly said High Risk, High Returns,
                and here is a picture of different types of possible investments comparing the risk and returns,
                choose the one for you and let me help you dig deep into one of your choices.
                As you see, index funds are good choices for less risk, we have some of popular ones on our homepage."""
                # st.image() # TODO
                with st.chat_message("assistant"):
                    st.markdown(res)
                    st.image("https://img.freepik.com/premium-vector/risk-vs-return-investment-types-investment-portfolio-balance-risk_518018-1920.jpg?w=1380")
                    st.image("https://www.investopedia.com/thmb/Ut5cfwsVdTrAg2fprVIqfFv1wXY=/750x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/INV-Asset-Classes-114-a82638558a344378aacd8eb1620a4481.jpg")
                st.session_state.messages.append({"role": "assistant", "content": res, "image": "https://www.investopedia.com/thmb/1Z6Z9Q1"})
    

            # elif (set(psplit) & begin_words):
            #     res = """Don't worry! I can help you get started!  
            #     I can provide you a full analysis of a stock just provide me the ticker"""
            #     # TODO
            #     with st.chat_message("assistant"):
            #         st.markdown(res)
            #     st.session_state.messages.append({"role": "assistant", "content": res})
            
            elif (set(psplit) & help_words):
                res = """I'll help you to my full capacity!  
                To start with analyzing a stock:  
                Ask us the latest data, the  best stratergy and future data,  
                Additionally, can also ask for the latest news of the stock, and also the major holders.
                To analyze a stock you look at the recent data, you also see how it has been performing in the past
                and then me guide to future predictions by the ML models, but always know that this is not enough, and just quants
                also look around for other factors like the latest news and also which big have the stocks as well.
                Try asking me these questions, and let me help you analyze.
                What is the recent data of AAPL ?  
                What is the best strategy for AAPL for maximum profit ?  
                What is the future data of AAPL ?  
                And maybe you can ask me about the latest news of AAPL, and also the major holders."""
                with st.chat_message("assistant"):
                    st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})  

            # 处理股票代码查询

            elif len(psplit) == 1 and prompt.isupper() and prompt[-1].isalpha():
                ticker = prompt
                st.session_state.ticker = ticker
                print("TICKER:", ticker)
                with st.chat_message("assistant"):
                    res = "Thankyou, for providing me the ticker!"
                    st.markdown(res)

                st.session_state.messages.append({"role": "assistant", "content": res})
                try: # TODO ADD
                    psplinew = st.session_state.unsolved
                    print(psplinew)
                    check_and_answer(psplinew)
                except Exception:
                    with st.chat_message("assistant"):
                        res = f"What can I help you with analyzing {ticker} today!"
                        st.markdown(res)
                
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
            
            elif (set(psplit) & stratergy_words) and "Sharpe" in psplit or 'sharpe' in psplit:
                ticker = st.session_state.ticker
                with st.spinner("Backtesting on 5 years data..."):
                    if st.session_state.strat_data is None:
                        st.session_state.strat_data = strat.run_strats(ticker)
                    analysis, graph = strat.high_sharpe_ratio(ticker, st.session_state.strat_data)
                    response = "We have backtested on last five years data and this strategy works the best:"
                    analysis = analysis.split("\n")
                    with st.chat_message("assistant"):
                            st.markdown(response)
                            for line in analysis:
                                st.markdown(line)
                            for g in graph:
                                st.pyplot(g)
                st.session_state.messages.append({"role": "assistant", "content": response, "analysis": analysis, "graph_list": graph})

            elif (set(psplit) & stratergy_words) and ((set(psplit) & bestst_words) or (set(psplit) & maxst_words)) and ("Profit" in psplit or "profit" in psplit or "Return" in psplit or "return" in psplit or "returns" in psplit):
                # TODO give the data for the stratergy with max annualised return
                ticker = st.session_state.ticker
                with st.spinner("Backtesting 4 strategies on 5 years data..."):
                    if st.session_state.strat_data is None:
                        st.session_state.strat_data = strat.run_strats(ticker)
                
                    analysis,graph = strat.max_prof(ticker, st.session_state.strat_data)
                    analysis = analysis.split("\n")
                    response = "We have backtested on last five years data and this strategy works the best:"
                    with st.chat_message("assistant"):
                        st.markdown(response)
                        for line in analysis:
                            st.markdown(line)
                        for g in graph:
                            st.pyplot(g)
                st.session_state.messages.append({"role": "assistant", "content": response, "analysis": analysis, "graph_list": graph})


            elif (set(psplit) & stratergy_words) and ((set(psplit) & riskst_words) or "Volatility" in psplit or 'Risky' in psplit):
                ticker = st.session_state.ticker
                with st.spinner("Backtesting 4 strategies on 5 years data..."):
                    if st.session_state.strat_data is None:
                        st.session_state.strat_data = strat.run_strats(ticker)
                    analysis, graph = strat.less_risk_only(ticker, st.session_state.strat_data)
                    analysis = analysis.split("\n")
                    response = "We have backtested on last five years data and this strategy works the best:"
                    with st.chat_message("assistant"):
                        st.markdown(response)
                        for i in analysis:
                            st.markdown(i)
                        for g in graph:
                            st.pyplot(g)
                st.session_state.messages.append({"role": "assistant", "content": response, "analysis": analysis, "graph_list": graph})
                # TODO give the stratergy with leaset risk and its graph
            
            elif (set(psplit) & stratergy_words) and (set(psplit) & fullst_words): 
                ticker = st.session_state.ticker
                with st.spinner("Backtesting 4 strategies on 5 years data..."):
                    response = "I backtest on five years data of four strategies and this is the full analysis for you."
                    if st.session_state.strat_data is None:
                        st.session_state.strat_data = strat.run_strats(ticker)
                    analysis = strat.get_analysis(ticker, st.session_state.strat_data)
                    with st.chat_message("assistant"):
                        st.markdown(response)
                        st.markdown(analysis)
                st.session_state.messages.append({"role": "assistant", "content": response, "analysis": analysis})

                # TODO give the stratergy with full analysis and its graph
                #   处理使用策略的历史数据请求
                # elif any(word in psplit for word in asking_words) and (set(psplit) & previous_data_words) and ("data" in psplit):
        
                # with st.spinner("Analyzing stock data..."):
                #     analysis = strat.get_analysis(st.session_state.ticker)
                    # with st.chat_message("assistant"):
                    #     st.markdown(response)
                    #     st.markdown(analysis)
                
                # st.session_state.messages.append({"role": "assistant", "content": response})
                # # print(response)
                # st.session_state.messages.append({"role": "assistant", "content": response})
            
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
                            response2 = f"The best model of {ticker} is {best_model_info['model']} with MAE(Mean Absolute Error):{best_model_info['mae']}."           
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
                            st.markdown(f"The best model for {ticker} is {best_model} with MAE(Mean Absolute Error): {best_mae:.4f}")
                            st.pyplot(comparefig)
                        st.session_state.messages.append({"role": "assistant", "content": response, "graph": fig})
                
            
                    # print(response)
                # st.session_state.messages.append({"role": "assistant", "content": response})
            
            elif "Why" in psplit or "why" in psplit:
                if "news" in psplit or "news?" in psplit or "News" in psplit:
                    res = """News related to a specific company, such as the release of a company's earnings report,
                    can also influence the price of a stock (particularly if the company is posting after a bad quarter).
                    In general, strong earnings generally result in the stock price moving up (and vice versa).  
                    *Why is it benefial for indiviuals?*  
                    For individuals, financial news is beneficial because it provides information that can affect their personal finances and investment portfolio. Financial news is essential to financial professionals, as it can have a positive, negative and neutral effect on investing, trading and transactions."""
                
                elif "major" in psplit or "Major" in psplit or "holders" in psplit or "Holders" in psplit:
                    res = """By watching the trading activity of corporate insiders and large institutional investors, it's easier to get a sense of a stock's prospects.  
                    Stocks with a large amount of institutional ownership are often looked upon favorably.
                    Large entities frequently employ a team of analysts to perform detailed and expensive financial research before the group purchases a large block of a company's stock.
                    The big Company arent in for a loss, so are't you, so might follow their path, BUT by baby footsteps."""
                
                elif set(psplit) & growth_rate_words:
                    res = """Growth rates are important because they affect the cash flows, profitability, and risk of a business, and therefore influence its valuation. Higher growth rates usually imply higher value, but also higher uncertainty and volatility.
                    ompanies with high growth rates typically sell for higher valuation multiples. Investors often determine what level of return they need on an investment, called a discount rate.  
                    **It measure a company's revenue increase and potential to expand.**
                    It is the percentage change of a given metric over a given period of time."""

                with st.chat_message("assistant"):
                    st.markdown(res)
                    st.session_state.messages.append({"role": "assistant", "content": res})





            # 处理情感分析请求
            elif any(word in psplit for word in sentiment_words):
                ticker = st.session_state.ticker
                if ticker:
                    sentiment = analyze_stock_sentiment(ticker)
                    if sentiment is "positive":
                        response = f"The sentiment for stock {ticker} is {sentiment}.You can  buy it."
                    elif sentiment is "negative":
                        response = f"The sentiment for stock {ticker} is {sentiment}.Prefer not to buy it."
                    else:
                        response = f"The sentiment for stock {ticker} is {sentiment}.Can't really say to buy or not."
        
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
                    llm_model(prompt)
                    

            elif "thankyou" in psplit or "Thankyou" in psplit or "Thank you" in psplit:
                response = "You're welcome! I'm always here to help you with your stock analysis and any doubts."
                with st.chat_message("assistant"):
                    st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

            else:
                with st.spinner("Getting response for you .."):
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
                st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})

            '''
            if response:
                with st.chat_message("assistant"):
                    st.markdown(response)
            '''

        except Exception as e:
            print(e)
            error_message = "I'm sorry, I couldn't process your request. Could you please try again?"
            st.session_state.messages.append({"role": "assistant", "content": error_message})
            with st.chat_message("assistant"):
                st.markdown(error_message)




# 处理用户输入
global prompt
if prompt := st.chat_input("Ask us!!",key="input2"):
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
