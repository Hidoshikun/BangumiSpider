# -*- coding: utf-8 -*-

from multiprocessing import Process, Queue
from get_content import muti_content_crawler
from get_url import get_url
from sql_work import write_database
from setting import PROCESS_MAX

import threading


if __name__=="__main__":
    url_queue = Queue()
    data_queue = Queue()

    threading.Thread(target=get_url, args=(url_queue,)).start()

    for i in range(0, PROCESS_MAX):
        Process(target=muti_content_crawler, args=(url_queue, data_queue)).start()

    threading.Thread(target=write_database, args=(data_queue,)).start()