import pandas as pd
import jieba
import os

# 设置数据目录和预处理后数据保存目录
data_dir = 'data'
pre_data_dir = 'pre_data'

# 如果预处理数据保存目录不存在，则创建
if not os.path.exists(pre_data_dir):
    os.makedirs(pre_data_dir)

# 读取data目录下的所有CSV文件
for file_name in os.listdir(data_dir):
    if file_name.endswith('.csv'):
        file_path = os.path.join(data_dir, file_name)
        
        # 读取CSV文件
        df = pd.read_csv(file_path)

        # 数据清洗
        df.drop(['date', 'ip 属地'], axis=1, inplace=True)
        df = df[df['评分'].apply(lambda x: x in range(1, 6))]

        # 文本预处理
        def preprocess_text(text):
            # 分词
            words = jieba.cut(text)
            # 去除停用词
            stop_words = set(['的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一个', '我们', '你', '自己', '会', '到', '去', '国', '这', '那', '有', '种', '中', '也', '地', '面', '看', '而', '后', '一', '同', '因为', '和', '有'])
            words = [word for word in words if word not in stop_words and word.strip() != '']
            return ' '.join(words)

        # 应用预处理函数
        df['comments'] = df['comments'].apply(preprocess_text)

        # 保存预处理后的数据到pre_data目录
        pre_file_path = os.path.join(pre_data_dir, file_name)
        df.to_csv(pre_file_path, index=False)