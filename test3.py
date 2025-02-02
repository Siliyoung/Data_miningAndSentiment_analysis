import time
import random
import re
import pandas as pd
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

if __name__ == '__main__':
    # 示例：获取携程页面
    id = "遇龙河景区"#景点名称
    url = "https://you.ctrip.com/sight/yangshuo702/22081.html?scene=online"
    # ChromeDriver 配置
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 无头模式
    options.add_argument('--disable-gpu')  # 禁用 GPU 加速
    driver = webdriver.Chrome(service=Service('./chromedriver.exe'), options=options)

    try:
        driver.get(url)
        time.sleep(4)
        # 获取地址
        address = driver.find_elements(By.CSS_SELECTOR, '.baseInfoText')[0]
        # 获取总页数
        ddl = driver.find_elements(By.CSS_SELECTOR, '.ant-pagination')
        for t in ddl:
            ddl1 = t.text.split("\n")[-2]
        j = 1

        # 获取地址
        address = driver.find_elements(By.CSS_SELECTOR, '.ant-pagination')

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

    finally:
        driver.quit()

    # 保存数据到 CSV
    data = pd.DataFrame({
        "date": timeList,
        "ip 属地": ip,
        "评分": scoreList,
        "comments": comments
    })
    data.to_csv(f"data/result_{id}_{address}.csv", encoding='utf-8', index=False)

    print("数据已保存至 CSV 文件")
