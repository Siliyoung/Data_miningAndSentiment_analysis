from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_heat_score_text(driver, url):
    try:
        driver.get(url)  # 进入景区页面
        wait = WebDriverWait(driver, 20)  # 设置最长等待时间为20秒

        # 显式等待heatScoreText元素可见
        heat_score_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.commentScoreNum')))
        
        # 获取元素的文本内容
        heat_score_text = heat_score_element.text
        print(f"heatScoreText元素存在，文本内容为：{heat_score_text}")
        
        # 将提取的文本转换为浮点数
        heat_score = float(heat_score_text)
        print(f"提取的热度分数为：{heat_score}")
        
    except Exception as e:
        print(f"在获取heatScoreText元素文本时发生错误：{e}")

# 初始化WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 无头模式
options.add_argument('--disable-gpu')  # 禁用 GPU 加速
driver = webdriver.Chrome(service=Service('./chromedriver.exe'), options=options)

# 测试URL
test_url = "https://you.ctrip.com/sight/guilin28/5925.html?"
test_heat_score_text(driver, test_url)

# 退出WebDriver
driver.quit()