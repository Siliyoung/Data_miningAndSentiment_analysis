import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_sight_details(driver, sight_url):
    # 进入景区页面并获取地址信息
    driver.get(sight_url)
    
    try:
        # 等待地址元素出现，确保页面已经加载
        address_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'p.baseInfoText'))
        )
        address = address_element.text
    except Exception as e:
        address = "无地址"  # 如果没有找到地址信息，给出默认值
        print(f"Error extracting address: {e}")
    
    return address

def test_sight_data_extraction():
    # 设置 Chrome 无头模式
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 无头模式
    options.add_argument('--disable-gpu')  # 禁用 GPU 加速
    driver = webdriver.Chrome(service=Service('./chromedriver.exe'), options=options)

    try:
        # 目标网页
        url = "https://you.ctrip.com/sight/guilin28/s0-p1.html"  # 请根据实际情况修改
        driver.get(url)
        time.sleep(3)  # 等待页面加载

        # 查找所有景区的 div 元素
        div_elements = driver.find_elements(By.CSS_SELECTOR, '.titleModule_name__Li4Tv')

        # 测试：输出所有抓取到的景区名称、URL 和等级
        for div in div_elements:
            try:
                # 获取景区名称和链接
                a_tag = div.find_element(By.TAG_NAME, 'a')
                sight_name = a_tag.text
                sight_url = a_tag.get_attribute('href')
                
                # 获取景区等级，加入异常处理，若无等级则默认显示“无等级”
                try:
                    level_span = div.find_element(By.CLASS_NAME, 'titleModule_level-text-view__40Dbg')
                    sight_level = level_span.text
                except:
                    sight_level = "无等级"  # 如果没有找到等级信息，赋予默认值

                # 获取景区地址信息
                address = get_sight_details(driver, sight_url)

                # 打印数据
                print(f"景区名称: {sight_name}")
                print(f"景区链接: {sight_url}")
                print(f"景区等级: {sight_level}")
                print(f"景区地址: {address}")
                print("-" * 40)

            except Exception as e:
                print(f"Error extracting data: {e}")

    finally:
        driver.quit()

# 运行测试
if __name__ == "__main__":
    test_sight_data_extraction()
