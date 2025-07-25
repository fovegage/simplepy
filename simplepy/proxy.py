import os
import string
import time
import zipfile

import requests
from pypac import PACSession, get_pac
from simplepy import logger
from simplepy.config import PROXY_PWD, PROXY_USER, PROXY_PORT, PROXY_HOST
from simplepy.db import get_redis_pool

redis_pool = get_redis_pool()


def create_proxy_auth_extension(scheme='http'):
    """
    selenium动态插件代理
    :param scheme:
    :return:
    """
    base_path = os.path.dirname(__file__)
    plugin_path = os.path.join(base_path, f'resources/proxy_auth_plugin.zip')
    manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Abuyun Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

    background_js = string.Template(
        """
        var config = {
            mode: "fixed_servers",
            rules: {
                singleProxy: {
                    scheme: "${scheme}",
                    host: "${host}",
                    port: parseInt(${port})
                },
                bypassList: ["foobar.com"]
            }
          };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "${username}",
                    password: "${password}"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
        );
        """
    ).substitute(
        host=PROXY_HOST,
        port=PROXY_PORT,
        username=PROXY_USER,
        password=PROXY_PWD,
        scheme=scheme,
    )

    with zipfile.ZipFile(plugin_path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return plugin_path


def channel_proxy():
    """
    隧道代理ip
    """
    proxy_host = 'http-dynamic.xiaoxiangdaili.com'
    proxy_port = 10030
    proxy_username = '845155349958119424'
    proxy_pwd = 'T8PCmL1g'

    proxy_meta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxy_host,
        "port": proxy_port,
        "user": proxy_username,
        "pass": proxy_pwd,
    }

    proxies = {
        'http': proxy_meta,
        'https': proxy_meta,
    }
    return proxies


def pac_proxy():
    """
    https://blog.csdn.net/guangdeshishe/article/details/123326214
    http://nathanlvzs.github.io/Web-Request-Through-PAC-Proxy.html
    https://pypac.readthedocs.io/en/latest/index.html
    :return:
    """
    # 使用代理
    proxy = 'xxx.xxx.x.xx:8080'
    proxies = {
        'http': 'http://' + proxy,
        'https': 'https://' + proxy
    }
    url = ''
    # 使用PAC自动代理
    pac = get_pac(url='http://xxx.xxx.x.xx:8080/xxx.pac')
    pac_session = PACSession(pac)  # 解析pac文件
    response = pac_session.get(url)


def random_ip():
    """
    redis返回代理IP
    :return:
    """
    proxies = {
        "http": "http://" + redis_pool.get('temp_ip').decode(),
        "https": "http://" + redis_pool.get('temp_ip').decode()
    }
    return proxies


def get_proxy():
    """
    小象代理返回格式：
    {"code":200,"success":true,"data":[{"ip":"xxx.xxx.xxx.xxx","port":xx,"during":60}],"msg":"操作成功"}
    Returns:
    """
    url = f'https://api.xiaoxiangdaili.com/ip/get?appKey={PROXY_USER}&appSecret={PROXY_PWD}&cnt=&wt=json'
    while True:
        try:
            rep = requests.get(url).json()
            logger.info(rep)
        except Exception as e:
            logger.error(e)
            continue
        else:
            redis_pool.set('temp_ip', str(rep['data'][0]['ip']) + ":" + str(rep['data'][0]['port']))
        finally:
            redis_pool.ping()
            time.sleep(11)


def switch_proxy():
    os.system('pppoe-stop;pppoe-start')
