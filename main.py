#爬虫 main.py 
import time
import re
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

import warnings
warnings.filterwarnings('ignore')

timeList = [] # 发表时间
ip = [] # ip 属地
scoreList = [] # 评分
comments = [] # 评论文本
def getData(driver, ddl1, j):
    '''获取数据'''
    times = driver.find_elements(By.CSS_SELECTOR, '.commentTime')
    scores = driver.find_elements(By.CSS_SELECTOR, '.averageScore')[1:]
    comment = driver.find_elements(By.CSS_SELECTOR, '.commentDetail')

    for c, t, s in zip(comment, times, scores):
        try:
            timeList.append(re.findall(r'(\d{4}-\d{1,2}-\d{1,2})', t.text)[0])
            ip.append(re.findall(r"：(.*)", t.text)[0])
            scoreList.append(re.findall(r"(.*)分", s.text)[0])
            comments.append(c.text)
        except:
            pass
    print(f"共{int(ddl1)}页，第{j}页下载完成...")
    # print("111")
if __name__ == '__main__':
    id = input("遇龙河景区")#景点名称
    url = input("https://you.ctrip.com/sight/yangshuo702/22081.html?scene=online")# 下载链接
    i = 500

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36')
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(4)
        #bad_review_button = driver.find_element(By.CSS_SELECTOR, 
        #'#commentModule > div.hotTags > span:nth-child(5)')
        #bad_review_button.click()
        #time.sleep(2) # 等待页面加载差评数据
        # 获取总的页码
        ddl = driver.find_elements(By.CSS_SELECTOR, '.ant-pagination')
        for t in ddl:
            ddl1= t.text.split("\n")[-2]
        j = 1

        while True:
            t1 = random.uniform(1, 2)

            getData(driver, ddl1, j) # 获取数据
            j += 1
            # 翻页
            element = driver.find_element(By.CSS_SELECTOR, '.ant-pagination-next a')
            driver.execute_script("arguments[0].click();", element)
            if j == int(ddl1) +1 or j > i:
                break
            time.sleep(t1)
    finally:
        driver.close()
    # save
    data = pd.DataFrame({ "date": timeList, "ip 属地": ip, "评分": scoreList, "comments": comments })
    data.to_csv(f"data/result_{id}.csv", encoding='utf8')
    print("done")