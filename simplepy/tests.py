import requests

from simplepy import logger
from simplepy.web import CommonSel


def proxy_test(ip, gfw=False):
    """
    78.38.100.121:8080
    :param ip:
    :return:
    """
    proxies = {
        "http": f"http://{ip}",
        "https": f"http://{ip}"
    }
    if gfw:
        target_url = 'https://www.google.com/'
    else:
        target_url = "https://httpbin.org/ip"
    rep = requests.get(url=target_url, proxies=proxies, timeout=5)
    logger.info(rep.status_code)
    logger.info(rep.text)


class TestSel(CommonSel):
    def start(self, **kwargs):
        url = "https://httpbin.org/ip"
        self.driver.get(url)
        logger.info(self.driver.page_source)


def selenium_proxy_test():
    proxy = '128.1.156.143:57814'
    ts = TestSel(proxy=proxy, headless=TestSel)
    ts.start()


if __name__ == '__main__':
    selenium_proxy_test()
