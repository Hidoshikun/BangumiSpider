# BangumiSpider
A simple spider for bangumi.tv.

一个用于爬取Bangumi网站动画数据的小爬虫。

## 程序构成

爬虫程序主要分为四个部分：代理获取get_proxy.py、目录获取get_url.py、内容获取get_content.py、数据库写入sql_work.py。

主程序main.py启动后生成两个队列url_queue与data_queue用于保存待爬取的url与已经爬取完成的页面数据data，同时启动一个目录获取线程，PROCESS_MAX个内容获取进程，1个数据库写入线程，

### 代理获取
该部分依赖于github上的开源项目[IPProxyPool](https://github.com/qiyeboy/IPProxyPool)
 ，下载后运行其中的IPProxy.py文件，通过对127.0.0.1:8000进行访问便能获取稳定健壮的代理ip。该部分包含了ip代理能否到达Bangumi的测试与对无效ip的删除。

### 目录获取
从Bangumi的动画排行页面往后进行翻页即可获取所有收录的动画的链接集合，当翻页后发现获取的集合为空时判断已经获取了所有的动画详情链接。获取的动画详情链接加入到url_queue队列中。

### 内容获取
每个进程启动THREAD_MAX个进程，从url_queue中获取待爬取的动画详情页url，使用Beautifulsoup的css选择器进行选择，获取动画的标题、评分、标签、导演、上映日期等数据，生成包含相关数据的字典，加入到data_queue队列中。

### 数据库写入
使用MySQLdb访问本地的MySQL数据库，从data_queue中获取数据并进行解析，执行sql插入语句将其插入到数据库中。

爬虫进行了简单的异常捕获与处理，能在较长时间内稳定的运行。通过使用IPProxyPool项目提供的健壮的代理，观察爬虫的效率在4进程20线程的设置下已经能达到100页/秒的速度，相较于以前静态ip代理池十几页每秒的速度已经是相当快了，晚上不断网的情况下单台机子一天能爬取14w+的数据。当然这里面应该还有加快速度的方法，日后可以尝试一下增加更多的爬取进程，或者增加写入进程的数量观察一下。

## 运行方式
1. 运行[IPProxyPool](https://github.com/qiyeboy/IPProxyPool) 主程序IPProxy.
2. setting中设置好最大进程、最大线程数目，设置好数据库链接相关参数。 
3. 运行BangumiSpider主程序main.

## 不足之处
项目对异常状态的捕获比较笼统，异常的处理也只是简单的重试，日后可以自定义一些错误类型加入程序中，方便日后的维护与错误排查。

以后可以考虑加入断点续爬功能，在项目停止后将断点记录到文件中，下一次开始的时候程序从文件中读取断点的位置重新开始爬取，总不能让笔记本不休不眠的跑几天…
