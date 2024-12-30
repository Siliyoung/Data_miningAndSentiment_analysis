import os
import pandas as pd
import re

# === 配置参数 ===
data_dir = "processed_data"  # 原始数据目录
output_dir = "processed_data2"  # 处理后保存的目录
min_comment_length = 1  # 最小评论长度，设为1以确保保留短评

# 创建保存目录
os.makedirs(output_dir, exist_ok=True)

# === Step 1: 数据清理和预处理函数 ===
def preprocess_review(review):
    # 去除表情符号（确保不影响正常文字）
    # review = re.sub(r'[\U0001F600-\U0001F64F'
    #                 r'\U0001F300-\U0001F5FF'
    #                 r'\U0001F680-\U0001F6FF'
    #                 r'\U0001F700-\U0001F77F'
    #                 r'\U0001F780-\U0001F7FF'
    #                 r'\U0001F800-\U0001F8FF'
    #                 r'\U0001F900-\U0001F9FF'
    #                 r'\U0001FA00-\U0001FA6F'
    #                 r'\U0001FA70-\U0001FAFF'
    #                 r'\U00002702-\U000027B0'
    #                 r'\U000024C2-\U0001F251]', '', review)
    # 去除多余空格
    review = review.strip()
    return review

def is_valid_comment(comment):
    # 检查评论是否有效
    return len(comment) >= min_comment_length

# === Step 2: 遍历文件并处理 ===
file_list = [f for f in os.listdir(data_dir) if f.endswith(".csv")]

for file in file_list:
    # 加载数据
    file_path = os.path.join(data_dir, file)
    df = pd.read_csv(file_path)
    
    # 数据预处理
    df["comments"] = df["comments"].fillna("").astype(str).apply(preprocess_review)
    
    # 过滤无效评论
    df = df[df["comments"].apply(is_valid_comment)]
    
    # 格式化数据为目标样式
    formatted_data = df[["评分", "comments"]]
    
    # 保存处理后的文件
    output_file_path = os.path.join(output_dir, file)
    formatted_data.to_csv(output_file_path, index=False, header=True, quoting=1, encoding="utf-8")  # quoting=1 确保双引号包裹字段
    
    print(f"处理完成: {file} -> {output_file_path}")

print(f"所有文件已处理完毕，结果保存在 {output_dir} 文件夹中。")
