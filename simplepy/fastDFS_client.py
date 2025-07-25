#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：codeline
@File    ：fastDFS_client.py
@Author  ：fovegage
@Email   ：fovegage@gmail.com
@Date    ：2022/6/10 13:30
"""
import io

from fdfs_client.client import Fdfs_client

config = {
    'host_tuple': ('192.168.12.126',),
    'port': 22122,
    'timeout': 30,
    'name': 'Tracker Pool'
}

client = Fdfs_client(config)
# f = io.BytesIO(b'ksl')

# result = client.upload_appender_by_buffer(b'two', 'csv')
# client.append
# result = client.list_all_groups()
result = client.append_by_buffer(b'asas\n', b'group1/M00/00/00/wKgMfmKjAaiEESmHAAAAAHcM_P4720.csv')
# f.close()
# client.append_by_file()
# client.append_by_filename()
# result = client.upload_by_filename('test.csv')
# client.download_to_file()
print(client)
print(result)

"""
{'Group name': b'group1', 'Remote file_id': b'group1/M00/00/00/wKgMfmKi3yqAOpE3AAAAApiu_FM794.csv', 'Status': 'Upload successed.', 'Local file name': 'test.csv', 'Uploaded size': '2B', 'Storage IP': b'192.168.12.126'}

"""


# TODO: sqlite 存储  或者 consul 进行文件的存储
