from urllib.parse import urlencode
from urllib.request import Request, urlopen

import simplejson

from simplepy import logger


def post(url: str, body: str or dict, headers: dict = None, log=False):
    """
    解决request不能发送中文的问题
    后续爬虫使用该骚操作
    https://www.cnblogs.com/pipipguo/p/15063608.html
    """
    if isinstance(body, str):
        data = body.encode()
    elif isinstance(body, dict):
        data = urlencode(body).encode()
    else:
        data = body
    req = Request(
        url=url,
        data=data,
        headers=headers if headers else {},
        method='POST')

    res = urlopen(url=req, timeout=12)
    with res:
        content = simplejson.loads(res.read())
    if log:
        logger.info(content)
    return content


if __name__ == '__main__':
    post('https://httpbin.org/post', {"a": 1}, log=True)
