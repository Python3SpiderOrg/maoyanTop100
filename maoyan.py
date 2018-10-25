# !usr/bin/env python3
# encoding:utf-8
"""
@project = maoyan
@file = maoyan
@author = 'Easton Liu'
@creat_time = 2018/10/25 11:54
@explain: 使用正则表达式爬取猫眼电影网TOP100

"""
import requests
import re
import json
from time import sleep
def get_html(url):
    headers = {
        r'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
    }
    response = requests.get(url,headers=headers)
    if response.status_code==200:
        response.encoding='utf-8'
        return response.text
    return None
def parse_html(response):
    pattern = '<dd>.*?class="board-index.*?>(\d+)</i>.*?<img.*?data-src="(.*?)".*?title="(.*?)".*?"releasetime">(.*?)</p>.*?"integer">(.*?)</i>.*?fraction">(.*?)</i>'
    results = re.findall(pattern,response,re.S)
    for result in results:
        yield {
            'index':result[0],
            'image':result[1],
            'title':result[2],
            'releasetime':result[3],
            'integer':result[4],
            'fraction':result[5]
        }
def write_to_file(content):
    with open('output.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')
def main(offset):
    url = r'http://maoyan.com/board/4?offset={}'.format(offset)
    html = get_html(url)
    for item in parse_html(html):
        print(item)
        write_to_file(item)
if __name__=='__main__':
    for i in range(10):
        main(offset=i*10)
        sleep(1)