import time
import random
import re
import pandas as pd
import os  # 导入os模块用于文件判断
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# 数据列表
timeList = []  # 发表时间
ip = []  # IP 属地
scoreList = []  # 评分
comments = []  # 评论文本

def getData(driver, ddl1, j):
    '''获取数据'''
    times = driver.find_elements(By.CSS_SELECTOR, '.commentTime')
    scores = driver.find_elements(By.CSS_SELECTOR, '.averageScore')[1:]  # 评分可能从第二个元素开始
    comment = driver.find_elements(By.CSS_SELECTOR, '.commentDetail')

    for c, t, s in zip(comment, times, scores):
        try:
            # 提取评论时间
            timeList.append(re.findall(r'(\d{4}-\d{1,2}-\d{1,2})', t.text)[0])
            # 提取IP属地
            ip.append(re.findall(r"：(.*)", t.text)[0])
            # 提取评分
            scoreList.append(re.findall(r"(.*)分", s.text)[0])
            # 提取评论内容
            comments.append(c.text)
        except Exception as e:
            print(f"Error on page {j}: {e}")
    print(f"共{ddl1}页，第{j}页下载完成...")

def read_sight_data(csv_file):
    """读取CSV文件并返回景区名称和链接的列表"""
    sight_data = pd.read_csv(csv_file, encoding='utf-8')
    return sight_data[['景区名称', '景区链接']]

def sanitize_filename(filename):
    """替换文件名中的非法字符"""
    return re.sub(r'[\/:*?"<>|]', '_', filename)

if __name__ == '__main__':
    # 读取sight_data.csv文件
    sight_data = read_sight_data('sight_data.csv')  # 读取CSV文件

    # ChromeDriver 配置
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 无头模式
    options.add_argument('--disable-gpu')  # 禁用 GPU 加速
    driver = webdriver.Chrome(service=Service('./chromedriver.exe'), options=options)

    try:
        # 遍历CSV中的每个景区
        for index, row in sight_data.iterrows():
            id = row['景区名称']  # 景区名称
            url = row['景区链接']  # 景区链接

            # 检查文件是否已经存在
            address = driver.get(url)  # 进入景区页面
            time.sleep(4)
            address_text = driver.find_elements(By.CSS_SELECTOR, '.baseInfoText')[0].text
            address_text = sanitize_filename(address_text)  # 清理地址中的非法字符

            # 文件名
            filename = f"data/result_{id}_{address_text}.csv"

            if os.path.exists(filename):
                print(f"文件 {filename} 已存在，跳过该景区...")
                continue  # 跳过该景区，处理下一个景区

            # 获取总页数
            ddl = driver.find_elements(By.CSS_SELECTOR, '.ant-pagination')
            for t in ddl:
                ddl1 = t.text.split("\n")[-2]
            j = 1

            while True:
                t1 = random.uniform(1, 2)
                getData(driver, ddl1, j)  # 获取数据
                j += 1
                # 翻页
                element = driver.find_element(By.CSS_SELECTOR, '.ant-pagination-next a')
                driver.execute_script("arguments[0].click();", element)
                if j > int(ddl1):
                    break
                time.sleep(t1)

            # 保存数据到 CSV
            result_data = pd.DataFrame({
                "date": timeList,
                "ip 属地": ip,
                "评分": scoreList,
                "comments": comments
            })
            result_data.to_csv(filename, encoding='utf-8', index=False)
            print(f"数据已保存至 CSV 文件: {filename}")

            # 清空数据列表，准备抓取下一个景区
            timeList.clear()
            ip.clear()
            scoreList.clear()
            comments.clear()

    finally:
        driver.quit()
