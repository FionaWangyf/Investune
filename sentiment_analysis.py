import pandas as pd
import tweetnlp
import sys

# 加载情感分析模型
model = tweetnlp.load_model('sentiment', multilingual=True)

# 定义情感分析函数
def analyze_sentiment(tweet):
    result = model.sentiment(tweet)
    return result['label']  # 确保返回标签

# 综合情感结果函数
def aggregate_sentiments(sentiments):
    sentiments = list(sentiments)  # 将 Series 转换为列表
    positive = sentiments.count('positive')
    neutral = sentiments.count('neutral')
    negative = sentiments.count('negative')
    
    if positive > negative and positive > neutral:
        return 'positive'
    elif negative > positive and negative > neutral:
        return 'negative'
    else:
        return 'neutral'

# 分析单个股票代码的情感
def analyze_stock_sentiment(stock_code):
    # 构建文件名
    dataset = f'{stock_code}.csv'
    
    # 读取数据集
    try:
        df = pd.read_csv(dataset)
    except FileNotFoundError:
        print(f"Dataset for stock code {stock_code} not found.")
        return
    
    # 假设推文内容在'full_text'列中
    tweets = df['full_text']
    
    # 对每条推文进行情感分析
    sentiments = tweets.apply(analyze_sentiment)
    
    # 综合情感结果
    final_sentiment = aggregate_sentiments(sentiments)
    return final_sentiment

# 从命令行获取股票代码
if len(sys.argv) < 2:
    print("Usage: python script.py STOCK_CODE")
else:
    stock_code = sys.argv[1]
    final_result = analyze_stock_sentiment(stock_code)
    if final_result:
        print(f"The overall sentiment for {stock_code} is {final_result}")
