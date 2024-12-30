import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

def read_sight_data(csv_file):
    """读取CSV文件并返回景区名称和链接的列表"""
    sight_data = pd.read_csv(csv_file, encoding='utf-8')
    return sight_data[['景区名称', '景区链接']]

def extract_numbers(text):
    """从文本中提取数字"""
    return re.findall(r'\d+', text)

def extract_float(text):
    # 使用正则表达式匹配小数
    pattern = r'\b\d+\.\d+\b'
    match = re.search(pattern, text)
    if match:
        return float(match.group(0))
    else:
        return None

def main():
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

            driver.get(url)  # 进入景区页面
            wait = WebDriverWait(driver, 10)  # 显式等待最多10秒

            print(id)  # 测试

            try:
                # 尝试获取地址信息
                address_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.baseInfoText')))
                address_text = address_element.text
                sight_data.at[index, "地址"] = address_text
                print(address_text)
            except Exception as e:
                print(f"处理 {id} 时发生错误: {e}")
                sight_data.at[index, "地址"] = "错误"

            try:
                # commentCount 获取点评数
                comment_count_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.commentCount')))
                comment_count_text = comment_count_element.text
                comment_count_numbers = extract_numbers(comment_count_text)
                if comment_count_numbers:
                    sight_data.at[index, "点评数"] = int(comment_count_numbers[0])  # 假设最大的数字是点评数
                else:
                    sight_data.at[index, "点评数"] = "无点评"
                print(comment_count_numbers[0])
            except Exception as e:
                print(f"处理 {id} 时发生错误: {e}")
                sight_data.at[index, "点评数"] = "错误"

            
            try:
                # commentScoreNum评分
                comment_score_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.commentScoreNum')))
                comment_score_text = comment_score_element.text
                comment_score = extract_float(comment_score_text)
                sight_data.at[index, "评分"] = comment_score
                print(comment_score)
            except Exception as e:
                print(f"处理 {id} 时发生错误: {e}")
                sight_data.at[index, "评分"] = "错误"


    finally:
        driver.quit()  # 退出WebDriver

    # 保存数据到 CSV
    sight_data.to_csv("update_sight_data.csv", encoding='utf-8', index=False)
    print("数据已更新")

if __name__ == '__main__':
    main()