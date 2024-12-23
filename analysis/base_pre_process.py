import pandas as pd
import jieba

# 读取CSV文件
df = pd.read_csv('your_file.csv')

# 数据清洗
df.drop(['date', 'ip 属地'], axis=1, inplace=True)

# 确保评分列中的值是有效的
df = df[df['评分'].apply(lambda x: x in range(1, 6))]

# 文本预处理
def preprocess_text(text):
    # 分词
    words = jieba.cut(text)
    # 去除停用词
    stop_words = set(['的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一个', '我们', '你', '自己', '会', '到', '去', '国', '这', '那', '有', '种', '中', '也', '地', '面', '看', '而', '后', '一', '同', '因为', '和', '有'])
    words = [word for word in words if word not in stop_words]
    return ' '.join(words)

# 应用预处理函数
df['comments'] = df['comments'].apply(preprocess_text)

# 保存预处理后的数据
df.to_csv('preprocessed_data.csv', index=False)