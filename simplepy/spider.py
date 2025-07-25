import os

import pandas as pd
from tenacity import retry, stop_after_attempt

from simplepy import logger
from simplepy.decorators import get_callback_path
from simplepy.utils import csv_save, base_download


# TODO:缓存包引入  requests-cache

def pandas_task():
    """
    多进程/多线程运行基础方法
    Returns:

    """


@get_callback_path
def loop(func, target, filename, method="dict", log=True, to_excel=False, total=10000):
    """
    通用处理器
    @retry(stop=stop_after_attempt(100))
    def detail(page):
        url = f'http://ghzyj.gz.gov.cn/JGG/xcapi/ghgs/list?page={page}&limit=10&opeClass=&itemName=%E7%94%B5%E6%A2%AF&gsArea=&passForeAft=&notSl=1&publish_id='
        rep = requests.get(url, headers=default_headers()).json()['records']
        return rep
    Args:
        func: 传入上述方法  必须为数组对象
        target: 目标位置  __file__ 也可是其他目录
        filename: 文件名
        total:
        to_excel:
        log:
        method: 数据形式

    Returns:

    """
    for page in range(1, total):
        logger.info(f"第{page}页，共{total}页")
        rep = func(page=page)
        # dict: {}
        if method == 'dict':
            if len(rep) == 0 or rep is None:
                break
            for item in rep:
                if log:
                    logger.info(item)
                csv_save(item, target, filename)
        else:
            # 存储类似pandas_html读取运行后的dataframe
            csv_save(rep, target, filename)
    if to_excel:
        main_path = os.path.split(target)[0]
        df = pd.read_csv(os.path.join(main_path, filename))
        df.to_excel(f"{main_path, filename}.xlsx", index=False)


@retry(stop=stop_after_attempt(100))
def pandas_html(df_index, url, debug=True):
    """
    返回最小粒度，具体循环交给外部
    Args:
        df_index:
        url:
        debug:

    Returns:

    """
    html = base_download(url)
    df = pd.read_html(html)[df_index]
    if debug:
        logger.info(df)
    return df
