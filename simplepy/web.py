#!/usr/bin/python3
import os
import time

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from loguru import logger
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from simplepy import LIB_PATH, IS_LINUX, IS_WINDOWS
from simplepy.decorators import get_callback_path
from simplepy.helpers import download_chrome_driver
from simplepy.proxy import create_proxy_auth_extension
from simplepy.resources import stealth
from simplepy.utils import csv_save


# TODO: 插件websocket爬虫
class SelMixin:

    @staticmethod
    def plugin():
        proxy_auth_plugin_path = create_proxy_auth_extension()
        return proxy_auth_plugin_path


class CommonSel(SelMixin):
    """
    https://blog.csdn.net/wkb342814892/article/details/81591394
    通用selenium处理
    https://sites.google.com/chromium.org/driver/downloads
    # 查看可执行文件路径：chrome://version/
    macos：/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome
    windows：chrome.exe -remote-debugging-port=9222 --user-data-dir="E:\chrome\s1"  --incognito --window-size=414,896
    centos：yum 安装后可以直接运行
    """

    def __init__(self, remote=None, phone=False, no_img=False, proxy=None, channel_proxy=False,
                 channel_proxy_info=None, plugin=None, virtual=False,
                 headless=False, window_size=None, cache_dir=None, traceless=False, img=True):
        """
        https://www.cnblogs.com/kaibindirver/p/11432850.html
        https://www.html.cn/doc/chrome-devtools/remote-debugging/
        https://www.shuzhiduo.com/A/6pdD2ZQOJw/
        TODO：chromedriver单独作用
        chromedriver --whitelisted-ips=""

        :param phone: 手机模式，远程模式不生效
        :param no_img: 不加载图片
        :param proxy: 使用代理
        :param channel_proxy: 使用隧道代理
        :param channel_proxy_info:
        :param headless: 无头浏览器
        :param window_size: 知道浏览器大小
        :param cache_dir: 缓存目录
        :param traceless: 无痕模式
        :param virtual: 虚拟化屏幕
        """

        # 下载chrome driver
        self.check_chrome()

        chrome_options = Options()
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        base_path = os.path.dirname(__file__)
        # 使用无头浏览器
        if headless:
            chrome_options.add_argument("--headless")
        # –incognito 隐身模式
        if traceless:
            chrome_options.add_argument('–-incognito')
        # --blink-settings=imagesEnabled=false # 不加载图片, 提升速度
        if not img:
            chrome_options.add_argument('--blink-settings=imagesEnabled=false')

        if virtual:
            # https://blog.csdn.net/wkb342814892/article/details/81591394
            # https://blog.csdn.net/freeking101/article/details/84994242
            display = Display(visible=False, size=(800, 600))
            display.start()
        # 启用缓存
        if cache_dir:
            cache_path = os.path.join(base_path, 'resources/cache')
            if not os.path.exists(cache_path):
                os.makedirs(cache_path)
            chrome_options.add_argument('--user-data-dir=' + f'{cache_path}')

        # 自定义插件
        if plugin:
            chrome_options.add_extension(plugin)

        # 普通代理 selenium代理的意义在于，传入代理ip，监听接口数据
        # 注意系统证书的安装
        if proxy:
            chrome_options.add_argument(f"--proxy-server={proxy}")
        # 隧道代理
        if channel_proxy and channel_proxy_info:
            chrome_options.add_extension(self.plugin())

        if phone and not remote:
            chrome_options.add_experimental_option("mobileEmulation", {"deviceName": "iPhone 6"})
            chrome_options.add_argument(
                'user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/101.0.4951.58 Mobile/15E148 Safari/604.1'
            )
        else:
            chrome_options.add_argument(
                'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
            )

        if no_img:
            chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

        if window_size:
            # 1280x1024
            chrome_options.add_argument('--window-size={}'.format(window_size))
        else:
            chrome_options.add_argument("--start-maximized")

        # remote 访问
        # '127.0.0.1:9222'
        if remote:
            chrome_options.add_experimental_option("debuggerAddress", remote)
        else:
            if os.name == 'posix':
                chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
            else:
                chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
                chrome_options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

        # 操作句柄
        if IS_WINDOWS:
            # windows
            self.driver = webdriver.Chrome(
                executable_path=f"{os.path.join(base_path, 'chrome_driver/chromedriver.exe')}",
                chrome_options=chrome_options
            )
        elif IS_LINUX:
            # centos
            # chrome_options.add_argument('--disable-gpu')
            self.driver = webdriver.Chrome(
                executable_path=f"{os.path.join(base_path, 'chrome_driver/chromedriver')}",
                chrome_options=chrome_options
            )
        else:
            # mac
            execute_path = f"{os.path.join(base_path, 'chrome_driver/chromedriver')}"
            self.driver = webdriver.Chrome(
                executable_path=execute_path,
                chrome_options=chrome_options
            )

        # 防止特征检测
        # with open(f"{os.path.join(base_path, 'resources/stealth.min.js')}") as f:
        #     js = f.read()
        js = stealth

        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": js
        })

    def soup(self, selector):
        return BeautifulSoup(self.driver.page_source, 'lxml').select(selector)

    @staticmethod
    def check_chrome():
        path = os.path.join(LIB_PATH, 'chrome_driver')
        if not os.path.isdir(path):
            os.makedirs(path)
            download_chrome_driver(path)

    def switch_iframe(self):
        """
        切换 iframe
        Returns:

        """
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))

    @staticmethod
    def debug(timeout=10000000):
        """
        调试
        Args:
            timeout:

        Returns:

        """
        time.sleep(timeout)

    def wait_next(self, name, method='xpath', timeout=120):
        """
        等待函数
        Args:
            name: 解析表达式
            method:
            timeout:

        Returns:

        """
        driver_wait = WebDriverWait(self.driver, timeout)
        if method == 'xpath':
            flag = By.XPATH
        elif method == 'id':
            flag = By.ID
        elif method == 'css':
            flag = By.CSS_SELECTOR
        else:
            flag = By.TAG_NAME
        driver_wait.until(
            EC.presence_of_element_located((flag, name)))

    def slide(self, height=1000000000):
        """
        进度条下滑
        Returns:

        """
        js_bottom = f"var q=document.documentElement.scrollTop={height};"
        self.driver.execute_script(js_bottom)

    @get_callback_path
    def yield_table(self, name, func, cols, bak=False, **kwargs):
        """
        动态传入一个爬虫主体方法 追加写入数据
        只需要关注主题业务代码的适配即可
        Args:
            name:
            func:
            cols: 列名数组
            **kwargs:
            bak:

        Returns:

        """
        path = kwargs.get('path')
        df = pd.read_csv(os.path.join(path, name))

        for idx, item in df.iterrows():
            try:
                result = func(item.url)
                logger.info(f"第{idx + 1}条，共{df.shape[0]}条")
                logger.info(result)
                if bak:
                    per = dict(zip(cols, result))
                    csv_save(per, path, f"{name}-bak-done")
            except Exception as e:
                logger.error(e)
                result = [np.nan] * len(cols)
            try:
                df.loc[idx, cols] = result
            except ValueError:
                continue

        logger.info(f'文件保存在：{path} 路径下')
        df.to_excel(f'{os.path.join(path, name)}-spider-done.xlsx', index=False)

    def loop(self):
        pass

    def execute(self):
        pass

    def start(self, **kwargs):
        pass


class CommonFirefox:
    def __init__(self, path, url, proxy=None, ua=None):
        self.url = url
        self.proxy = proxy  # ip:port
        self.path = path
        self.ua = ua
        # chrome 是 options  firefox 是 profile
        profile = FirefoxProfile()
        profile.set_preference('network.proxy.type', 1)
        if self.proxy:
            ip, port = self.proxy.split(':')
            profile.set_preference('network.proxy.http', ip)
            profile.set_preference('network.proxy.http_port', int(port))
            profile.set_preference('network.proxy.ssl', ip)
            profile.set_preference('network.proxy.ssl_port', int(port))
        if self.ua:
            profile.set_preference('general.useragent.override', ua)
        self.driver = webdriver.Firefox(profile, executable_path=self.path)
        self.driver.set_page_load_timeout(80)
        self.driver.set_script_timeout(80)

    def execute(self):
        pass


if __name__ == '__main__':
    print(os.path.dirname(__file__))
