# -*- coding: utf-8 -*-

import requests
import random

def get_proxy():
    while True:
        i = random.randint(0, 4)
        proxy_item = requests.get('http://127.0.0.1:8000/?types=0&count=5&country=国内',
                                  timeout=5).json()[i]
        ip = proxy_item[0]
        port = proxy_item[1]
        proxy = ip + ":" + str(port)

        if test_proxy(proxy) == 1:
            print("使用代理： " + proxy)
            return proxy


def test_proxy(proxy):

    html = requests.get("http://bangumi.tv/subject/110467", proxies=proxy).text

    if "SHIROBAKO" in html:
        return 1
    else:
        print("代理被ban，从代理池中删除...")
        del_proxy(proxy)
        return 0


def del_proxy(proxy):
    ip = proxy.split(":")[0]
    result = requests.get("http://127.0.0.1:8000/delete?ip="+ip, timeout=5).json()
    if result[1] == 1:
        print("删除代理成功")
    else:
        print("删除代理失败，代理已经不在ip池中")


if __name__ == "__main__":
    bgm_url = "http://bangumi.tv/"
    html = requests.get(bgm_url, proxies = get_proxy()).text
    head_str = '<body class="bangumi bangumiNeue">'
    if head_str in html:
        print("success")

