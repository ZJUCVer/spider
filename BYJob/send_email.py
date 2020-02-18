"""
邮件发送最新爬取结果
"""
import os
import yagmail


def get_new_result(result_dir):
    """
    获取最新的爬取结果
    :param result_dir: 结果目录
    :return: 最新爬取结果
    """
    file_list = os.listdir(result_dir)
    file_list.sort(key=lambda file: os.path.getmtime(result_dir + "/" + file))
    return result_dir + "/" + file_list[-1]


def send_email(new_result):
    """
    发送邮件
    :param new_result: 最新爬取结果
    :return: None
    """
    yag = yagmail.SMTP(user="写入发送邮箱", password="写入邮箱授权码（注意不是密码）", host='写入邮件服务器地址')
    receiver = '写入接收邮箱（多个接收邮箱时用列表即可）'
    subject = '写入邮件主题'
    contents = '写入邮件正文'
    yag.send(receiver, subject, contents, new_result)


def main():
    dir_path = os.getcwd() + '/results'
    result = get_new_result(dir_path)
    send_email(result)

if __name__ == '__main__':
    main()
