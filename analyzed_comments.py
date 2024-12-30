import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob

# === Step 1: 加载和整合数据 ===
# 定义数据目录和文件列表
data_dir = "data"
file_list = [f for f in os.listdir(data_dir) if f.endswith(".csv")]

# 合并所有文件
all_data = []
for file in file_list:
    file_path = os.path.join(data_dir, file)
    # 提取景区名和地址
    scenic_spot, address = file.replace("result_", "").replace(".csv", "").split("_")
    df = pd.read_csv(file_path)
    df["scenic_spot"] = scenic_spot  # 添加景区名
    df["address"] = address  # 添加地址
    all_data.append(df)

# 合并为一个DataFrame
data = pd.concat(all_data, ignore_index=True)

# === Step 2: 数据清洗 ===
# 去除空值并清洗评论内容
data.dropna(subset=["comments"], inplace=True)
data["cleaned_comments"] = data["comments"].str.replace(r"[^\w\s]", "", regex=True).str.strip()

# === Step 3: 情感分析 ===
def analyze_sentiment(text):
    """对文本进行情感分析"""
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

data["sentiment_score"] = data["cleaned_comments"].apply(analyze_sentiment)
data["sentiment_label"] = data["sentiment_score"].apply(
    lambda x: "positive" if x > 0 else "negative" if x < 0 else "neutral"
)

# === Step 4: 景区间比较 ===
# 计算每个景区的情感分布
sentiment_distribution = data.groupby("scenic_spot")["sentiment_label"].value_counts(normalize=True).unstack()

# 计算平均评分
average_rating = data.groupby("scenic_spot")["评分"].mean()

# === Step 5: 数据可视化 ===
# 情感分布可视化
plt.figure(figsize=(12, 6))
sentiment_distribution.plot(kind="bar", stacked=True, colormap="viridis", alpha=0.8)
plt.title("Sentiment Distribution by Scenic Spot")
plt.ylabel("Proportion")
plt.xlabel("Scenic Spot")
plt.xticks(rotation=45)
plt.legend(title="Sentiment")
plt.tight_layout()
plt.show()

# 平均评分可视化
plt.figure(figsize=(10, 5))
average_rating.plot(kind="bar", color="skyblue", alpha=0.85)
plt.title("Average Ratings by Scenic Spot")
plt.ylabel("Average Rating")
plt.xlabel("Scenic Spot")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# === Step 6: 保存结果 ===
data.to_csv("analyzed_comments.csv", index=False)
