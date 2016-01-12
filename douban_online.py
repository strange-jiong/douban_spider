#-*-coding:utf-8-*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib2
import re
from bs4 import BeautifulSoup
import time
import math


def delpunc(s):
    exclude = ',/\\();:"\'._~!#$%^&*{}[]?><'
    s = ''.join(x for x in s if x not in exclude)
    return re.sub(u"[，。！？【】（）]", "", s)
# print delpunc(a)
i = 0
a = 0
for i in range(0, 160):
    html = 'http://www.douban.com/online/tag/?start=%d' % (i)
    i = i + 160
    print html
    content = urllib2.urlopen(html, timeout=1000).read()
    soup = BeautifulSoup(content)
    foundtags = soup.find(class_="tag-table").findAll('td')
    file = open('1.txt', 'w')
    for tagtag in foundtags:
        tag = tagtag.a.string
        file.write(str(tag.encode('utf-8')) + "\n")
        # print tag
        num = tagtag.span.string
        # print type(num)
        num = int(re.findall(r'\d+', num)[0])
        lim = num / 10 + 1
        j = 0
        for j in range(0, lim + 1):
            url = ('http://www.douban.com/online/tag/' + tag).encode('utf-8')
            url = (url + '?start=%d') % (j * 10)
            j = j + 1
            print url, j
            content1 = urllib2.urlopen(url, timeout=1000).read()

            soup1 = BeautifulSoup(content1)
            tags1 = soup1.findAll("h3")
            for tagtag1 in tags1:
                a += 1
                tagtag1 = tagtag1.findAll('a')[0]
                tag1 = tagtag1.string
                tag2 = delpunc(tag1)

                print a, tag2.encode('utf-8').decode('utf-8')
                # a.append()
                # print a
                id = re.findall(
                    r'<a href="http://www.douban.com/online/(\d+)/">', str(tagtag1))[0]
                file.write(id + "\t")
                file.write(delpunc(str(tag2)) + "\t")
                eachhtml = 'http://www.douban.com/online/' + id + '/'
                content2 = urllib2.urlopen(eachhtml, timeout=1000).read()
                soup2 = BeautifulSoup(content2)
                org = soup2.find(class_='info')
                org = org.find('h3')
                uid = re.findall(
                    r'<a href="http://www.douban.com/people/(.*?)/">', str(org))
                if len(uid):
                    uid = uid[0]
                else:
                    uid = re.findall(
                        r'<a href="http://site.douban.com/(.*?)/">', str(org))[0]

                file.write(uid + '\t')
                phtml = eachhtml + 'participant'
                contentp = urllib2.urlopen(phtml, timeout=1000).read()
                soupp = BeautifulSoup(contentp)
                p = soupp.findAll('dd')
                for ptag in p:
                    pp = ptag.findAll('a')
                    puid = re.findall(
                        r'<a href="http://www.douban.com/people/(.*?)/', str(pp))[0]

                    file.write(puid + '\t')
                time.sleep(0.5)
                file.write('\n' + '\n')
            time.sleep(2)

file.close()
