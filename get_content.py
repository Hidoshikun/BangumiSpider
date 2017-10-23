# -*- coding: utf-8 -*-

import requests
from multiprocessing import Queue
from bs4 import BeautifulSoup
import time
from urllib import parse
import hashlib
import datetime

from setting import THREAD_MAX

from get_proxy import get_proxy

def content_crawler(url_queue, data_queue):
    print("爬虫线程启动...")

    while True:
        if url_queue.empty():
            time.sleep(1)

        else:
            try:
                url = parse.urljoin("http://bangumi.tv/", url_queue.get())
            except:
                print("抓取失败，重试中...")
            else:
                print("开始抓取: " + url)
                html = requests.get(url, proxies=get_proxy()).content
                data_get(html, url, data_queue)

    pass

def data_get(html, url, data_queue):
    soup = BeautifulSoup(html, "lxml")

    # 作品名
    name = soup.select('.nameSingle a')[0].get_text()
    # 类型
    broadcast_type = soup.select('.nameSingle small')[0].get_text()
    # 评分
    score = soup.select('.global_score .number')[0].get_text()
    # 标签
    tags = soup.select('.subject_tag_section .inner a')
    tag_list = ','.join([tag.get_text() for tag in tags])
    # 标签标注数目
    tagging_nums = soup.select('.subject_tag_section .inner small')
    tagging_num_list = ','.join([tagging_num.get_text() for tagging_num in tagging_nums])

    m = hashlib.md5()
    m.update(str(url).encode('utf-8'))
    id = m.hexdigest()

    dic = {'id': id, 'url': url, '作品名': name, '类型': broadcast_type, '评分': score, '标签': tag_list,'标签标注数目': tagging_num_list, \
           '中文名': 'None', '导演': 'None', '总导演': 'None', '副导演': 'None', '播放日期': 'None', '系列构成': 'None', '动画制作': 'None', \
           '脚本': 'None', '分镜': 'None', '演出': 'None', '作画监督': 'None', '原画': 'None', '制片人': 'None'}

    nodes = soup.select('#infobox li')

    for node in nodes:
        t = node.select('.tip')[0].get_text()

        if t == '中文名: ':
            # print(t+" get")
            dic['中文名'] = node.get_text().strip(t)

        elif t == '导演: ':
            # print(t+" get")
            dic['导演'] = ','.join([person.get_text() for person in node.select('a')])

        elif t == '总导演: ':
            # print(t+" get")
            dic['总导演'] = ','.join([person.get_text() for person in node.select('a')])

        elif t == '副导演: ':
            # print(t+" get")
            dic['副导演'] = ','.join([person.get_text() for person in node.select('a')])

        elif t == '放送开始: ' or t == '发售日: ' or t == '上映年度: ':
            # print(t+" get")
            try:
                convert_date = datetime.datetime.strptime(node.get_text().strip(t), "%Y年%m月%d日").date()
            except Exception as e:
                convert_date = datetime.datetime.now().date()

            dic['播放日期'] = convert_date

        elif t == '系列构成: ':
            # print(t+" get")
            dic['系列构成'] = ','.join([person.get_text() for person in node.select('a')])

        elif t == '动画制作: ':
            # print(t+" get")
            dic['动画制作'] = ','.join([person.get_text() for person in node.select('a')])

        elif t == '脚本: ':
            # print(t+" get")
            dic['脚本'] = ','.join([person.get_text() for person in node.select('a')])

        elif t == '分镜: ':
            # print(t+" get")
            dic['分镜'] = ','.join([person.get_text() for person in node.select('a')])

        elif t == '演出: ':
            # print(t+" get")
            dic['演出'] = ','.join([person.get_text() for person in node.select('a')])

        elif t == '作画监督: ':
            # print(t+" get")
            dic['作画监督'] = ','.join([person.get_text() for person in node.select('a')])

        elif t == '原画: ':
            # print(t+" get")
            dic['原画'] = ','.join([person.get_text() for person in node.select('a')])

        elif t == '制片人: ':
            # print(t+" get")
            dic['制片人'] = ','.join([person.get_text() for person in node.select('a')])

    data_queue.put(dic)


def muti_content_crawler(url_queue, data_queue):
    import threading

    for i in range(0, THREAD_MAX):
        threading.Thread(target=content_crawler, args=(url_queue, data_queue)).start()

if __name__ == "__main__":

    import threading

    url_queue = Queue()
    data_queue =Queue()

    def put_test(url_queue, data_queue):
        print("put")
        url_queue.put("http://bangumi.tv/subject/110467")
        content_crawler(url_queue, data_queue)

    def get_test(data_queue):
        print("get")
        dic = data_queue.get()
        print(dic)

    threading.Thread(target=put_test, args=(url_queue, data_queue)).start()
    print("put test started")

    threading.Thread(target=get_test, args=(data_queue,)).start()
    print("get test started")