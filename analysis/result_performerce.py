import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 设置情感分析结果数据目录
analysis_data_dir = 'analysis_data'

# 初始化一个空的DataFrame来存储所有数据
all_data = pd.DataFrame()

# 读取analysis_data目录下的所有CSV文件
for file_name in os.listdir(analysis_data_dir):
    if file_name.endswith('.csv'):
        file_path = os.path.join(analysis_data_dir, file_name)
        # 读取CSV文件
        df = pd.read_csv(file_path)
        # 将数据添加到all_data DataFrame中
        all_data = pd.concat([all_data, df], ignore_index=True)

# 假设我们想要按情感分类进行计数
sentiment_counts = all_data['sentiment'].value_counts()

# 创建情感分类的柱状图
plt.figure(figsize=(10, 6))
sentiment_counts.plot(kind='bar', color=['green', 'blue', 'red'])
plt.title('Sentiment Analysis Results')
plt.xlabel('Sentiment')
plt.ylabel('Counts')
plt.xticks(rotation=0)
plt.show()

# 如果我们想要更详细的分析，比如每个景点的情感分布
# 假设all_data中有一个'Attraction'列，表示景点名称
if 'Attraction' in all_data.columns:
    plt.figure(figsize=(12, 8))
    sns.countplot(x='Attraction', hue='sentiment', data=all_data, palette='deep')
    plt.title('Sentiment Distribution by Attraction')
    plt.xlabel('Attraction')
    plt.ylabel('Counts')
    plt.legend(title='Sentiment')
    plt.show()

# 保存图表到文件
plt.figure(figsize=(10, 6))
sns.heatmap(all_data.groupby(['Attraction', 'sentiment']).size().unstack(), annot=True, cmap='coolwarm')
plt.title('Sentiment Heatmap by Attraction')
plt.savefig('sentiment_heatmap.png')
plt.close()