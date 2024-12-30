import os
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# 初始化VADER情感分析器
analyzer = SentimentIntensityAnalyzer()

# 定义情感分析函数
def analyze_sentiment(text):
    if not isinstance(text, str):
        return 0
    sentiment = analyzer.polarity_scores(text)
    print(f"文本: {text} -> 情感分数: {sentiment}")  # 打印文本和情感分数
    return sentiment['compound']

# 定义情感分类函数
def classify_sentiment(score):
    if score >= 0.05:
        return 'positive'
    elif score <= -0.05:
        return 'negative'
    else:
        return 'neutral'

# 读取processed_data文件夹下的所有CSV文件
input_dir = "processed_data"
output_dir = "sentiment_analysis_results"
os.makedirs(output_dir, exist_ok=True)

# 遍历文件夹中的每一个CSV文件
for filename in os.listdir(input_dir):
    if filename.endswith(".csv"):
        # 读取CSV文件
        file_path = os.path.join(input_dir, filename)
        data = pd.read_csv(file_path)
        
        # 确保comments列为字符串类型，处理空值
        data['comments'] = data['comments'].fillna('').astype(str)
        
        # 对评论进行情感分析，获取复合分数
        data['sentiment_score'] = data['comments'].apply(analyze_sentiment)
        
        # 根据情感分数进行分类
        data['sentiment_category'] = data['sentiment_score'].apply(classify_sentiment)
        
        # 按景区名称（文件名）命名输出文件
        output_file = os.path.join(output_dir, f"sentiment_{filename}")
        
        # 保存结果到新的CSV文件
        data.to_csv(output_file, index=False)
        
        print(f"情感分析和分类已完成并保存到 {output_file}")

print("所有文件的情感分析和分类已完成。")
