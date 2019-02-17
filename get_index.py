# coding=utf-8

# with open('index.txt',encoding='utf-8') as f:
#     urls = ""
#     for l in f.readlines():
#         urls = urls + l[15:68]
#         print(l[15:65])

import requests
import os
from lxml import html
import re

def get_html(url):
    print(url)

    index = url[-10:-4]
    page = url[-1] + '.html'
    base_dir = 'misa.eto/smph/index/' + index + '/'
    # print(index)
    # print(base_dir)
    # print(page)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    raw_html = requests.get(url, headers=headers)

    html = handle_html(raw_html.content, index)

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    with open(base_dir + page,'w',encoding='utf-8') as f:
        f.write(html)

def handle_html(content, index):
    tree = html.fromstring(content)

    for l in tree.xpath('//*[@id="head"]'):
        l.getparent().remove(l)
    for l in tree.xpath('//*[@id="menu2"]'):
        l.getparent().remove(l)
    for l in tree.xpath('//*[@id="snsbtns"]'):
        l.getparent().remove(l)
    for l in tree.xpath('//*[@id="officialSNS"]'):
        l.getparent().remove(l)
    for l in tree.xpath('//*[@class="pcbtn"]'):
        l.getparent().remove(l)



    content = html.tostring(tree, method='html', encoding='utf-8')
    content = str(content, encoding='utf-8')

    content = re.sub('\\?p=1\\&amp;d={}'.format(index), '1.html', content)
    content = re.sub('\\?p=2\\&amp;d={}'.format(index), '2.html', content)
    content = re.sub('\\?p=3\\&amp;d={}'.format(index), '3.html', content)
    content = re.sub("http://blog.nogizaka46.com/", '../../../../', content)
    content = re.sub('php"', 'html"', content)
    content = re.sub('//www.google-analytics.com/analytics.js', '', content)
    content = re.sub('//j.wovn.io/1', '', content)
    content = re.sub('//img.nogizaka46.com/www/smph/img/fukidash.png', '', content)
    # save the num
    content = re.sub('smph/\\?d=(\d+)', 'smph/index/\\1/1.html', content)

    content = re.sub('misa.eto/smph/"', 'misa.eto/smph/index.html"', content)

    #print(content)
    return content

def create_url():
    urls = []
    with open('index.txt',encoding='utf-8') as f:
        for l in f.readlines():
            for i in range(1,4):
                urls.append(l[:-1]+'&p={}'.format(i))
        print(urls)
    return urls



urls = create_url()

for url in urls[21:]:
    get_html(url)