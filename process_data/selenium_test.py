# 导入所需模块
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pathlib import Path

# 设置Chrome浏览器的下载路径
chrome_options = Options()
BASE_DIR = Path(__file__).resolve().parent.parent
BASE_FILE_DIR = BASE_DIR / 'file'
chrome_options.add_experimental_option("prefs", {"download.default_directory": BASE_FILE_DIR.as_posix()})

# 启动Chrome浏览器
driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(1366,768)
# 打开需要下载文件的页面
driver.get("http://yjt.ah.gov.cn/public/column/9377745?type=4&catId=49550989&action=list")

# 找到搜索框
# 找到输入框并输入关键字
input_box = driver.find_element(By.ID, 'public_search_keywords')
input_box.send_keys("招标")

search_btn = driver.find_element(By.XPATH, "//input[@value='搜索']")
search_btn.click()




# 找到下载链接并点击
driver.find_element(By.XPATH, '//button[text()="Some text"]')