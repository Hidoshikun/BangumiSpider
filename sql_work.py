# -*- coding: utf-8 -*-

import MySQLdb
import queue
from setting import DATABASE_CONFIG
import datetime
import time

def write_database(data_queue):
    conn = MySQLdb.connect(host = DATABASE_CONFIG['host'], user = DATABASE_CONFIG['user'],
                               passwd = DATABASE_CONFIG['passwd'], db = DATABASE_CONFIG['db'],
                               charset = DATABASE_CONFIG['charset'])
    cursor = conn.cursor()

    insert_sql = """
        insert into animation_zwei (id, url, name, broadcast_type, score, tag_list, tag_num_list, \
        chinese_name, director, chief_director, sub_director, broadcast_time, series_composition, \
        studio, script, storyboard, episode_director, animation_director, animator, producer ) \
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    while True:
        if data_queue.empty():
            time.sleep(1)

        else:
            try:
                data = data_queue.get()

                params = (
                    data['id'], data['url'], data["作品名"], data['类型'], data['评分'], data['标签'], data['标签标注数目'], \
                    data['中文名'], data['导演'], data['总导演'], data['副导演'], data['播放日期'], data['系列构成'], \
                    data['动画制作'], data['脚本'], data['分镜'], data['演出'], data['作画监督'], data['原画'], data['制片人']
                )

                cursor.execute(insert_sql, params)
                conn.commit()

                print("写入完成: " + data['url'])

            except:
                print("写入出错，重试中...")


    conn.close()

if __name__ == "__main__":

    data_queue = queue.Queue()
    data = {'id': '5d91b4de9ffadeb86482855c34c0e018', 'url': 'http://bangumi.tv/subject/110467', '作品名': 'SHIROBAKO', '类型': 'TV', '评分': '8.8', '标签': 'P.A.WORKS,原创,2014年10月,励志,水岛努,白箱,TV,SHIROBAKO,动画制作,2014,横手美智子,青春,原创动画,水島努,百合,职场,业界,治愈,吉田玲子,2014年,日常,神作,ぽんかん⑧,梦想,半年番,TVA,搞笑,浜口史郎,科普,热血', '标签标注数目': '(1886),(876),(827),(761),(739),(695),(473),(453),(419),(245),(240),(226),(222),(217),(150),(41),(24),(20),(20),(19),(17),(17),(17),(11),(10),(9),(9),(9),(8),(8)', '中文名': '白箱', '导演': '水島努', '总导演': 'None', '副导演': 'None', '播放日期': datetime.date(2014, 10, 9), '系列构成': '横手美智子', '动画制作': 'P.A.WORKS', '脚本': '吉田玲子,横手美智子,浦畑達彦', '分镜': '成田歳法,岡村正弘,畑博之,駒井一也,篠原俊哉,倉川英揚,湖山禎崇,水島努,許琮,菅沼芙実彦,高村彰,かおり,柿本広大,平井義通', '演出': '菱川直樹,横田一平,畑博之,高島大輔,太田知章,熨斗谷充孝,倉川英揚,今泉賢一,水島努,許琮,菅沼芙実彦,湖山禎崇,かおり,守岡博,平牧大輔', '作画监督': '渡辺佳奈子,酒井智史,佐藤陽子,野田康行,齊藤佳子,川村夏生,鈴木理沙,川口千里,神崎舞人,朴允玉,西畑あゆみ,熊田明子,朱炫祐,容洪,今泉賢一,川面恒介,大東百合恵,秋山有希,森島範子,松坂定俊,宮川智恵子,佐野陽子,深澤謙二,武田牧子,徐正徳,関口可奈味,竹田欣弘,しまだひであき', '原画': '室井ふみえ,石井百合子,玄馬宣彦,井上俊之,渡邊政治,青木康哲', '制片人': '川瀬浩平,堀川憲司,永谷敬之'}

    data_queue.put(data)
    write_database(data_queue)