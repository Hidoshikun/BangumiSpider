# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import queue

from get_proxy import get_proxy

def get_url(url_queue):

    start_url = "http://bangumi.tv/anime/browser?sort=rank&page="

    flag = True
    n = 1

    while flag:
        requests_url = start_url + str(n)
        try:
            html = requests.get(requests_url, proxies=get_proxy()).content
        except:
            print("获取目录出错，重试中...")
        else:
            soup = BeautifulSoup(html, "lxml")
            hrefs = soup.select('#browserItemList li .subjectCover')

            if len(hrefs) == 0:
                flag = False
            else:
                for href in hrefs:
                    url = href.get("href")
                    url_queue.put(url)

            n += 1
            print("正在获取第" + str(n) + "页列表...")


    pass

if __name__ == "__main__":
    url_queue = queue.Queue()
    get_url(url_queue)