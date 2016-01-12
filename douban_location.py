# -*- coding: utf-8 -*-
"""
Created on Sun Sep 06 10:31:11 2015

@author: jiongwang

http://www.douban.com/location/xian/
任务描述：
1、抓取豆瓣同城栏目所有有关的活动信息，具体指标如下：
1）：抓取西安、北京、上海、深圳、武汉等城市
2）：抓取同城的音乐类、戏剧、讲座、聚会、电影、展览、运动、公益、旅行、其他等
3）：每一个活动需要获取：
活动名称、活动id、时间、地点、费用、类型、主办方、感兴趣的人、参加的人等
（其中感兴趣的人以只需抓取人名对应的uid）
2、数据存储格式要求：
1)每一个活动以一个txt文件存储，文件名命名规则为“地名_活动类型_活动id.txt”
2)文件内，以上各个字段分别各占一行，其中参加及感兴趣的人的uid单独一行，
uid之间以逗号（英文逗号）分隔。
抓取西安、北京、上海、深圳、武汉等城市

"""
import sys
reload(sys)
sys.setdefaultencoding("utf8")


import requests
import re
import time
import random
from lxml import etree


def spider():
    """
    应该没有什么bug，都调过了，在命令行中运行的乱码也已解决。
    代码写的比较粗糙，函数就一个spider()直接实现功能。
    """

    print '正在使用豆瓣同城活动爬虫工具。\n                      ——————————jiong'.encode('utf-8').decode('utf-8')

    destination = {'xian': '西安',  'beijing': '北京',
                   'shanghai': '上海', 'shenzhen': '深圳',
                   'wuhan': '武汉'}

    category = {'运动': 'sports', '旅行': 'travel',
                '公益': 'commonweal', '展览': 'exhibition',
                '音乐': 'music', '戏剧': 'drama',
                '讲座': 'salon', '聚会': 'party',
                '电影': 'film', '其它': 'others'}

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
                            AppleWebKit/537.36 (KHTML, like Gecko) \
                            Chrome/45.0.2454.99 Safari/537.36'}

    for city in destination:

        for kind in category:
            url1 = 'http://www.douban.com/location/' + city + \
                '/events/week-' + category[kind]
            r = requests.get(url=url1, headers=headers)

            html1 = r.text
            selector = etree.HTML(html1)            # 通过网页源代码 生成xpath对象
            event = selector.xpath(                 # 每一种分类页面
                '//*[@id="db-events-list"]/ul/li/div[2]/div/a/@href')

            file_name2 = destination[city] + '_' + kind + '.txt'

            file = open(unicode(file_name2, 'utf-8'), 'w')

            for each in event:  # 进入活动的具体页面
                html2 = requests.get(url=each, headers=headers).text
                event_selector = etree.HTML(html2)
                event_info = {}
                event_info['活动uid'] = each[-9:-1]
                event_info['活动名称'] = event_selector.xpath(
                    '//*[@id="event-info"]/div[1]/h1/text()')[0].strip()
                event_info['主办方'] = event_selector.xpath(
                    '//*[@id="event-info"]/div[1]/div[5]/a/text()')[0]
                event_info['地点'] = ''.join(event_selector.xpath(
                    '//*[@id="event-info"]/div[1]/div[2]/span[2]/span/text()'))
                event_info['时间'] = event_selector.xpath(
                    '//*[@id="event-info"]/div[1]/div[1]/ul/li/text()')[0]
                event_info['费用'] = event_selector.xpath(
                    '//*[@id="event-info"]/div[1]/div[3]/text()')[1].strip()
                event_info['类型'] = event_selector.xpath(
                    '//*[@id="event-info"]/div[1]/div[4]/a/text()')[0]
                event_info['感兴趣的人'] = event_selector.xpath(
                    '//*[@id="event-info"]/div[1]/div[6]/span[1]/text()')[0]
                event_info['参加的人'] = event_selector.xpath(
                    '//*[@id="event-info"]/div[1]/div[6]/span[3]/text()')[0]

                # 感兴趣的人的url
                url3 = each + 'wisher'
                html3 = requests.get(url=url3, headers=headers).text
                people_s1 = etree.HTML(html3)
                interest1 = people_s1.xpath(
                    '//*[@id="content"]/div/div[1]/div/div/dl/dt/a/@href')  # 得到的是url list
                # print interest1
                for index1, each_one1 in enumerate(interest1):
                    interest1[index1] = re.findall(
                        r'people/(.*)/', each_one1)[0]
                event_info['感兴趣的人_uid'] = ','.join(interest1)

                url4 = each + 'participant'  # 参与的人的url
                html4 = requests.get(url=url4, headers=headers).text
                people_s2 = etree.HTML(html4)
                interest2 = people_s2.xpath(
                    '//*[@id="content"]/div/div[1]/div/div/dl/dt/a/@href')  # 得到的是url list
                for index2, each_one2 in enumerate(interest2):
                    interest2[index2] = re.findall(
                        r'people/(.*)/', each_one2)[0]
                event_info['参加的人_uid'] = ','.join(interest2)

                file_name1 = destination[city] + '_' + \
                    event_info['类型'] + '_' + '.txt'

                # 命令行中给出运行信息
                print r'正在记录'.encode('utf-8').decode('utf-8'), destination[city].encode('utf-8').decode('utf-8'), event_info['类型'], event_info['活动uid'], r'的信息'.encode('utf-8').decode('utf-8'), '...'

                for key in event_info:
                    file.write(key)
                    file.write(': ')
                    file.write(event_info[key])
                    file.write('\n')
                file.write('\n')

                # 产生一个3至6秒的随机时间间隔
                time.sleep(random.randint(3, 6))
            file.close()
    a = raw_input('Just for stop\n      ----jiong')


def main():
    spider()

if __name__ == '__main__':
    main()
