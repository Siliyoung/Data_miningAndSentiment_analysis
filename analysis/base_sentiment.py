from snownlp import SnowNLP

# 读取预处理后的数据
df = pd.read_csv('preprocessed_data.csv')

# 情感分析
def sentiment_analysis(text):
    s = SnowNLP(text)
    if s.sentiments > 0.5:
        return 'positive'
    elif s.sentiments < 0.5 and s.sentiments > 0:
        return 'neutral'
    else:
        return 'negative'

# 应用情感分析函数
df['sentiment'] = df['comments'].apply(sentiment_analysis)

# 结果统计
sentiment_counts = df['sentiment'].value_counts()

print(sentiment_counts)

# 保存情感分析结果
df.to_csv('sentiment_analysis_results.csv', index=False)