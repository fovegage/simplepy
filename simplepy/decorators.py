import inspect
import os
import time
import traceback
from functools import wraps
from uuid import uuid1

from aiohttp.client_exceptions import ClientError, ServerTimeoutError
from requests.exceptions import HTTPError

from simplepy import logger


def trying(counts):
    """
     一个装饰器
     传入重试次数
     仅仅处理 http 异常
     多线程调用问题
     :return:
    """

    def request_dec(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 使用外部变量
            nonlocal counts
            while counts > 0:
                try:
                    result = func(*args, **kwargs)
                except HTTPError or ServerTimeoutError or ClientError:
                    counts -= 1
                    continue
                else:
                    return result

        return wrapper

    # 多次调用次数重置
    # 否则造成重试次数失效
    # del counts
    return request_dec


def get_callback_path(func):
    """
    获取调用path
    由调用者进行存储
    Returns:

    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        callback_path = traceback.extract_stack()[0].filename
        save_path = os.path.split(callback_path)[0]
        filename = os.path.split(callback_path)[1]
        kwargs.update({'path': save_path})

        suffix = os.path.splitext(filename)[0]
        if suffix + '.csv' in os.listdir(save_path):
            kwargs.update({'filename': suffix + str(uuid1()).split('-')[-1]})
        else:
            kwargs.update({'filename': suffix})
        return func(*args, **kwargs)

    return wrapper


def var2str(func):
    """
    变量转字符串
    Args:
        func:

    Returns:

    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        callers_local_vars = inspect.currentframe().f_locals.items()
        var = [[var_name for var_name, var_val in callers_local_vars if var_val is y] for y in vars]
        return func(*args, **kwargs)

    return wrapper


def loop_page(detail_func, total, start=1):
    """

    Args:
        start:
        total:
        detail_func:
    Returns:

    """

    def circle_page(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # loop(func, )
            for page in range(start, total + 1):
                kwargs['page'] = page
                result = func(*args, **kwargs)
                print(result)
                # 进入二级
            return

        return wrapper

    return circle_page


def get_time(fun):
    @wraps(fun)
    def inner(*arg, **kwarg):
        s_time = time.time()
        res = fun(*arg, **kwarg)
        e_time = time.time()
        logger.info('Fun Execute Total Cost: {}s'.format(e_time - s_time))
        return res

    return inner


def duration(func):
    """
    execute time decorate
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        total = end - start
        if total < 60:
            total = f"{round(total, 2)} seconds"
        else:
            total = f"{round(total / 60, 2)} minutes"
        return total

    return wrapper
