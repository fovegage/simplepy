import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

import requests
from tenacity import retry, stop_after_attempt

from simplepy import logger
from simplepy.decorators import get_time


class SDMixin:
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.7113.93 Safari/537.36',
        'range': 'bytes=0-100'
    }


class StreamDown(SDMixin):
    def __init__(self, url, name, save_path, slice_nums=50):
        self.url = url
        self.name = name
        self.save_path = save_path
        self.step_dict = {}
        self.lock = Lock()
        self.logger = logger
        self.init()
        self.slice_length(slice_nums)

    @retry(stop=stop_after_attempt(50))
    def init(self):
        """
        获取基础的流信息
        :return:
        """
        headers = requests.get(self.url, headers=self.headers, timeout=30).headers
        if not headers.get('Content-Range'):
            raise Exception('retry')
        return headers

    def get_content_range(self) -> int:
        stream_range = self.init().get('Content-Range')
        range_length = stream_range.split('/')[-1]
        return int(range_length)

    def slice_write(self, future):
        """
        执行具体任务函数
        :return:
        """
        is_except = future.exception()
        if is_except:
            # 异常控制
            # 加入队列
            return
        stream, byte = future.result()
        self.logger.info(f'正在写入{byte}')
        start = byte[0]
        write_path = os.path.join(self.save_path, f"{self.name}")
        if not os.path.exists(write_path):
            f = open(write_path, 'w')
            f.close()
        with open(write_path, 'r+b') as f:
            f.seek(start)
            f.write(stream)

    @retry(stop=stop_after_attempt(100))
    def download(self, byte):
        """
        是否需要加锁
        :param byte:
        :return:
        """
        # 有可能造成死锁的  当一个下载进程不成功 便会一直等待
        # self.lock.acquire()
        headers = {'range': f'bytes={byte[0]}-{byte[-1]}'}
        # self.lock.release()
        res = requests.get(self.url, headers=headers, timeout=60).content, byte
        return res

    def slice_length(self, num):
        """
        分割 content-length
        :param length:
        :param num:
        :return:
        """
        length = self.get_content_range()
        self.logger.info("文件总大小 ---> ", length)
        per = length // num
        for i in range(num):
            self.step_dict[i] = per * i, per * i + per
        if length % num != 0:
            step = (length // num) * num
            self.step_dict.update({num: (step, step + length % num)})

    @get_time
    def multi_down(self):
        tasks = []

        loop_range = self.step_dict.values()
        with ThreadPoolExecutor(200) as execute:
            for step_range in loop_range:
                result = execute.submit(self.download, step_range)
                tasks.append(result)
            for task in as_completed(tasks):
                task.add_done_callback(self.slice_write)


if __name__ == '__main__':
    # 文件模式
    # https://blog.csdn.net/Hardworking666/article/details/111490801
    # 测试
    # https://vepic-material.vizen.cn/museumcloud/pic/164793366600025017.JPG
    # https://ve-material.vizen.cn/museumcloud/video/164759313200068639.mp4
    # TODO: 修改为队列
    sd = StreamDown(
        'https://ve-material.vizen.cn/museumcloud/video/164759313200068639.mp4',
        '党的历程.mp4',
        r"./",
        100
    )
    sd.multi_down()
    print(sd.step_dict)
