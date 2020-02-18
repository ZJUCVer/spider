"""
requests+Ajax分析+根据json在线解析结果直接解析字典
"""
import os
from datetime import datetime
import json
import requests
from requests.exceptions import RequestException


def get_one_page(url):
    """
    获取一个页面
    :param url: 通过Ajax分析得到的页面url
    :return: 页面（json文本）
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return None
    except RequestException as e:
        print('Error', e.args)
        return None


def parse_one_page(_json):
    """
    解析一个页面
    :param _json: 页面（json文本）
    :return: 解析结果（generator）
    """
    items = _json.get('results')
    for item in items:
        yield {
            'title': item.get('title'),
            'publishTime': item.get('publishTime'),
            'endTime': item.get('endTime'),
            'workingPlace': item.get('workingPlaceString')
        }


def get_file_path():
    """
    利用创建时间为结果文件命名，获取结果文件保存路径
    :return: 结果保存路径
    """
    dir_path = os.getcwd() + '/results'
    file_name = "jobInfo {}.txt".format(datetime.strftime(datetime.now(), "%Y-%m-%d %H-%M-%S"))
    file_path = os.path.join(dir_path, file_name)
    return file_path


def write_to_file(content, file_path):
    """
    将爬取结果写入文件
    :param content: 爬取结果（字典格式）
    :param file_path: 结果保存路径
    """
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(offset, file_path):
    """
    抓取一页，将解析结果写入文件
    :param offset: 页码
    :param file_path: 结果保存路径
    """
    url = 'https://job.bupt.edu.cn/recruitment-datas/25/' + str(offset) + '/2.html'
    page = get_one_page(url)
    for item in parse_one_page(page):
        print(item)
        write_to_file(item, file_path)


if __name__ == '__main__':
    path = get_file_path()
    for i in range(1, 11):
        main(offset=i, file_path=path)
