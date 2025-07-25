#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：codeline
@File    ：html2pdf.py
@Author  ：fovegage
@Email   ：fovegage@gmail.com
@Date    ：2022/6/14 17:22
"""

import os

from PyPDF2 import PdfFileMerger
from pdfkit import from_string

"""
文档
brew install wkhtmltopd
pip install pdfkit
http://mknight.cn/Python%E6%89%B9%E9%87%8F%E8%BD%AC%E6%8D%A2HTML%E4%B8%BAPDF.html
"""

# pdfkit.from_url('https://emed.amegroups.cn/article/10969', 'out1.pdf')
import requests
from string import Template

template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
${content}
</body>
</html>

"""


def download():
    url = 'https://emed.amegroups.cn/webapi/articles/show'
    data = {"timestamp": "1655205772", "nonce": "Gp66G03bCo3Evlmj", "app_id": "1005", "version_id": "2",
            "token": "Basic eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhbWVBdXRoU2VydmVyIiwic3ViIjoiYW1lQ2xpZW50IiwiYXVkIjoiYW1lR3JvdXBzIiwiZXhwIjoxNjU2NDk3MjU5MDAwLCJpYXQiOjE2NTUyMDEyNTkwMDAsImp0aSI6IjcwNWNhZDBjOWZkMTMxNGNiMDBmYWEwNWQyZGY0ZWUzIiwidXNlciI6IjIwMjIwNjE0NkxOeGMiLCJzaWduZWQiOiI2MDI1NTYxOTRAcXEuY29tIiwicGVybWlzc2lvbiI6W10sInBob25lIjoiIiwiZW1haWwiOiI2MDI1NTYxOTRAcXEuY29tIiwidXNlcl9pZCI6Nzc4MzkwLCJmaXJzdF9uYW1lIjoiXHU1MzNmXHU1NDBkIiwibGFzdF9uYW1lIjoiXHU1MzNmXHU1NDBkIn0=.39e099aa5768d84f87aea40f34b894ae97c3df9b3d2bc3a89119240815b3e5d7",
            "article_id": "10969", "sign": "3b70c948d1bed8c01835d90dbb799262cd7ed238"}
    rep = requests.post(url, data=data).json()['data']
    title = rep.get('title')
    content = rep.get('content')
    rep_content = Template(template).substitute(
        content=content
    )
    print(rep_content)

    from_string(rep_content, f'temp/{title}.pdf')


def merge():
    """
    合并过加入章节目录
    :return:
    """
    target_path = '/Users/gaozhe/PycharmProjects/codeline/libs/simplepy/simplepy/temp'
    pdf_lst = [f for f in os.listdir(target_path) if f.endswith('.pdf')]
    pdf_lst = [os.path.join(target_path, filename) for filename in pdf_lst]

    file_merger = PdfFileMerger()
    for pdf in pdf_lst:
        file_merger.append(pdf)  # 合并pdf文件

    file_merger.write("merge.pdf")


if __name__ == '__main__':
    # download()
    merge()
