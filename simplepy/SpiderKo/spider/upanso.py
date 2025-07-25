import re

import requests

from SpiderKo.config import HEADERS
from SpiderKo.core.bitmap import Bit
from SpiderKo.core.db import ClientDb
from SpiderKo.utils import get_file_name

task_name = get_file_name(__file__)
table1 = 'upanso'
table2 = 'disk_user'
client1 = ClientDb('pans', table1)
client2 = ClientDb('pans', table2)


def spider(key):
    url = f'https://api.upanso.com/search/v1/key/{key}?what=disk&disk_type=ALL&time=ALL&size=300&page=1&key='
    rep = requests.get(url, headers=HEADERS).json()['data']['result']
    for item in rep:
        disk_id = item['disk_id']
        disk_user = item['disk_user']
        client2.create_or_query('disk_user', disk_user)
        client1.create_or_query('disk_id', disk_id, **item)


def task(i, bit: Bit):
    rep = requests.get(f'https://bbs.misiai.com/d/{i}', headers=HEADERS)
    content = rep.content.decode()
    pattern = re.compile('https://disk\.upanso\.com/main/searchKey/(\w+)"')
    if rep.status_code == 200:
        bit.set_bit(i)
        for item in pattern.findall(content):
            try:
                spider(item)
            except Exception as e:
                # 加入log
                print(e)
                continue


def index(name):
    bit = Bit(name)
    start = bit.bitmap()
    # 每天固定爬 100 不会超过100
    for i in range(start, start + 10):
        task(i, bit)
    # with ThreadPoolExecutor(10) as execute:
    #     for i in range(start, start + 10):
    #         execute.submit(task, i, bit)


if __name__ == '__main__':
    # index()
    print(__file__)
