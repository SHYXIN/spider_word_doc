# 导入所需模块
import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pathlib import Path
from lxml import etree
from selenium.common.exceptions import NoSuchElementException
import time
import pickle
space_rule_list = [r'\s+', r'\\n', r'\\t', r'\\u3000', r'\n', r'\\ufeff', r'\ufeff', r'\u200b', r'\\u200b']

def exclude_illegal_text(origin_text_list, pattern_rule_str, **kwargs):
    """div中传入的结果text()，返回分句"""
    part_name = kwargs.get('part_name')
    p_split_rule = r'[，。；]'
    # garbled_rule = r'[A-Za-z\-=]{10}'
    # filter_style_text = ['FONT-FAMILY', 'WordSection1', 'alert', 'nameArr', 'style.display',
    #                      'font-family', 'font-size', 'margin-top', 'TRS_Editor']
    not_text_tag = ['script', 'style', ]
    # 如果想排除表格text_element.getparent().iterancestors() 迭代出所有的祖先进行排除
    stop_tag_text_list = [text_element for text_element in origin_text_list if
                          text_element.getparent().tag not in not_text_tag]
    #  # 可以通过getparent，然后再iterancestors迭代所有父标签
    # for idx, parent_element in enumerate(text_element.getparent().iterancestors()):
    # span_text_list = [i for i in ori_text_list if i and not regex.findall('|'.join(filter_style_text), i)]
    ori_no_space_text_list = []
    table_rule = {'table', 'td', 'tr'}
    ori_no_space_table_text_list = []
    for span_text in stop_tag_text_list:
        in_table_tag = set([e.tag for e in span_text.getparent().iterancestors()]) & table_rule
        span_text = span_text.strip()
        span_no_text = re.sub(pattern_rule_str, '', span_text)
        if span_no_text:
            ori_no_space_text_list.append(span_no_text)
            if not in_table_tag:
                ori_no_space_table_text_list.append(span_no_text)
    span_concat_str = ''.join(ori_no_space_text_list)  # 连接起来
    stop_space_str = re.sub(pattern_rule_str, '', span_concat_str)  # 去除空格  未来可能要去掉
    # print(span_concat_str)
    # tag = re.findall(garbled_rule, span_concat_str)
    # if tag:
    #     print(tag)
    small_all_split_list = re.split(p_split_rule, stop_space_str) if stop_space_str else []  # 分成段
    res_dict = {'ori_no_space_text_list': ori_no_space_text_list,
                'small_all_split_list': small_all_split_list,
                'ori_no_space_table_text_list': ori_no_space_table_text_list,
                }
    return res_dict


# 设置Chrome浏览器的下载路径
chrome_options = Options()
# chrome_options.add_argument('--headless')  # 不要浏览器界面
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



page_num = 0
all_list = []


while page_num < 10:
    print(f'当前为第{page_num:^3}页')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    li_browser = driver.find_elements(By.XPATH, '//ul[@class="clearfix xxgk_nav_list"]/li')
    for li in li_browser:
        a = li.find_element(By.CSS_SELECTOR, 'a')
        a.click()
        driver.switch_to.window(driver.window_handles[-1])
        driver.close()

        print(1)
    breakpoint()

    content = driver.page_source.encode('utf-8')
    parse_html = etree.HTML(content)
    # ul = parse_html.xpath('//ul[@class="clearfix xxgk_nav_list"]')[0].xpath('li')

    li_list = parse_html.xpath('//ul[@class="clearfix xxgk_nav_list"]/li')
    all_list.extend(li_list)

    page_num +=1
    time.sleep(4)
    try:
        page_btn = driver.find_element(By.XPATH, "//a[@aria-label='跳转至下一页']")
        page_btn.click()
    except Exception as e:
        break
#
# # 将字典对象保存到文件中
# with open('my_dict.pickle', 'wb') as f:
#     pickle.dump(all_list, f)
#
# # 从文件中读取字典对象
# with open('my_dict.pickle', 'rb') as f:
#     all_list = pickle.load(f)

for li in all_list:
    print(exclude_illegal_text(li.xpath('.//text()'), '|'.join(space_rule_list)))

