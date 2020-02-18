"""
Selenium+pyquery解析
"""
import os
import json
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
from time import sleep

browser = webdriver.Chrome()
browser.maximize_window()
wait = WebDriverWait(browser, 10)
keyword = "酒精湿巾"
max_page = 5
dir_path = os.getcwd() + '/results'
file_name = "products {}.txt".format(datetime.strftime(datetime.now(), "%Y-%m-%d %H-%M-%S"))
file_path = os.path.join(dir_path, file_name)


def index_page(page):
    """
    抓取索引页
    :param page: 页码
    """
    print('正在爬取第', page, '页')
    try:
        url = 'https://search.jd.com/Search?keyword={}&enc=utf-8'.format(keyword)
        browser.get(url)
        # page>1时跳转页码
        if page > 1:
            # 下拉加载页码框
            browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            sleep(1)
            input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="J_bottomPage"]/span[2]/input')))
            submit = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="J_bottomPage"]/span[2]/a')))
            input.clear()
            input.send_keys(page)
            submit.click()
        # 等待页码跳转，检查条件为当前高亮显示的页码是否是当前页码
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#J_bottomPage .p-num .curr'), str(page)))
        # 分段下拉滚动条，加载商品图片
        height = browser.execute_script("return document.body.scrollHeight;")
        step = height / 10
        for i in range(10):
            browser.execute_script("window.scrollBy(0,{})".format(step))
            sleep(1)
        get_products()
    except TimeoutException as e:
        print('第', page, '页加载超时:', e.msg)


def get_products():
    """
    提取商品数据
    """
    html = browser.page_source
    doc = pq(html)
    # 调用items()方法得到一个生成器
    items = doc('ul.gl-warp.clearfix li').items()
    for item in items:
        product = {
            'image': item.find('.p-img img').attr('src'),
            'price': item.find('.p-price i').text(),
            'title': item.find('.p-img a').attr('title'),
            'comment': item.find('.p-commit a').text(),
            'shop': item.find('.p-shop a').text(),
        }
        print(product)
        write_to_file(product)


def write_to_file(content):
    """
    将爬取结果写入文件
    :param content: 爬取结果（字典格式）
    """
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main():
    """
    遍历每一页
    """
    for i in range(1, max_page + 1):
        index_page(i)
    browser.close()


if __name__ == '__main__':
    main()
