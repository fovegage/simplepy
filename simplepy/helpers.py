# coding: utf-8
import os

from simplepy import IS_WINDOWS

if IS_WINDOWS:
    import winreg

import requests

import nacos
from simplepy import IS_WINDOWS, logger, IS_LINUX
from simplepy.multi_download import StreamDown
from simplepy.utils import unzip_file, get_cmd_print
from simplepy.utils import request_post
from uuid import uuid1


def get_base_chrome_driver(version):
    data = [
        {
            "name": "chromedriver_linux64.zip",
            "url": f"https://registry.npmmirror.com/-/binary/chromedriver/{version}chromedriver_linux64.zip",
        },
        {
            "name": "chromedriver_mac64.zip",
            "url": f"https://registry.npmmirror.com/-/binary/chromedriver/{version}chromedriver_mac64.zip",
        },
        {
            "name": "chromedriver_mac64_m1.zip",
            "url": f"https://registry.npmmirror.com/-/binary/chromedriver/{version}chromedriver_mac64_m1.zip",
        },
        {
            "name": "chromedriver_win32.zip",
            "url": f"https://registry.npmmirror.com/-/binary/chromedriver/{version}chromedriver_win32.zip",
        }
    ]
    return data


def get_chrome_driver():
    html = requests.get('https://registry.npmmirror.com/-/binary/chromedriver/').json()
    main_version = get_chrome_version()[1]
    result = list(filter(lambda x: str(x.get('name')).startswith(main_version), html))[0].get('name')
    if IS_WINDOWS:
        plat_name = "chromedriver_win32.zip"
    elif IS_LINUX:
        plat_name = 'chromedriver_linux64.zip'
    else:
        plat_name = 'chromedriver_mac64_m1.zip'
    download_info = list(
        filter(lambda x: x.get("name") == plat_name, get_base_chrome_driver(result))
    )[0]
    download_url = download_info.get('url')
    download_name = download_info.get('name')
    return download_url, download_name


def download_chrome_driver(path):
    download_url, download_name = get_chrome_driver()
    sd = StreamDown(download_url, download_name, path, 20)
    sd.multi_down()
    file_name = os.path.join(path, download_name)
    unzip_file(file_name, path)
    if not IS_WINDOWS:
        logger.info('可执行文件')
        os.system(f'chmod 777 {file_name}')


def get_chrome_version():
    """
    https://blog.csdn.net/sinat_41870148/article/details/109263847
    :return:
    """
    try:
        if IS_WINDOWS:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Google\Chrome\BLBeacon')
            chrome_version = winreg.QueryValueEx(key, 'version')[0]
            return chrome_version, chrome_version.split('.')[0]
        elif IS_LINUX:
            # linux Google Chrome 102.0.5005.61
            chrome_version = get_cmd_print('google-chrome --version').split()[-1]
            return chrome_version, chrome_version.split('.')[0]
        else:
            # mac os
            # https://superuser.com/questions/1144651/get-chrome-version-from-commandline-in-mac
            chrome_version = get_cmd_print(
                '/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version'
            ).split()[-1]
            return chrome_version, chrome_version.split('.')[0]
    except Exception as e:
        logger.error("该操作系统未安装Chrome Browser", e)


def email_fetch():
    """
    临时邮箱获取
    :return:
    """
    url = 'http://24mail.chacuo.net/'
    cookie = 'Hm_lvt_ef483ae9c0f4f800aefdf407e35a21b3=1653793645; Hm_lpvt_ef483ae9c0f4f800aefdf407e35a21b3=1653793645; mail_ck=2; sid=5d7c5b0d20a2d81f6a185be60ffbb737da235054'
    data = {"data": "uawbjk62879", "type": "refresh", "arg": ""}
    result = request_post(url, data, cookie=cookie)
    print(result)


def config_callback(x):
    print(x)


def nacos_config_fetch():
    SERVER_ADDRESSES = "192.168.12.126:8848"
    NAMESPACE = "e8d634f2-9096-4a96-8b22-ce3d0cb6a359"
    # auth mode
    client = nacos.NacosClient(SERVER_ADDRESSES, namespace=NAMESPACE, username="nacos", password="nacos")

    # get config
    data_id = "user-api.yaml"
    group = "home"
    print(client.get_config(data_id, group))

    # client.add_config_watcher(data_id, group, config_callback)


def nacos_register_instance(service: str, ip: str, http_port: int, grpc_port: int, grpc=False, ephemeral=True):
    """

    :param service:
    :param ip:
    :param http_port:
    :param grpc_port:
    :param grpc: 是否grpc
    :param ephemeral: 是否临时实例
    :return:
    """
    if grpc:
        metadata = {
            "preserved.register.source": "SPRING_CLOUD",
            "gRPC.port": f'{grpc_port}'
        }
    else:
        metadata = {
            "preserved.register.source": "SPRING_CLOUD",
        }
    SERVER_ADDRESSES = "192.168.12.126:8848"
    NAMESPACE = "public"
    # auth mode
    client = nacos.NacosClient(
        server_addresses=SERVER_ADDRESSES,
        # endpoint="/health/check",
        namespace=NAMESPACE,
        username="nacos",
        password="nacos"
    )
    rsp = client.add_naming_instance(
        service_name=service,
        ip=ip,
        port=http_port,
        cluster_name='DEFAULT',
        group_name='DEFAULT_GROUP',
        metadata=metadata,
        ephemeral=ephemeral
    )
    print(rsp)


def nacos_deregster_instance(service: str, ip: str, port: int):
    """
    ephemeral应与注册时候保持一致，否则会删不掉
    :param service:
    :param ip:
    :param port:
    :return:
    """
    SERVER_ADDRESSES = "192.168.12.126:8848"
    NAMESPACE = "public"
    # auth mode
    client = nacos.NacosClient(
        server_addresses=SERVER_ADDRESSES,
        namespace=NAMESPACE,
        username="nacos",
        password="nacos"
    )
    res = client.remove_naming_instance(service, ip, port, ephemeral=False)
    logger.info(res)


def consul_register(name: str, ip: str, port: int, method='http'):
    """
    文档
    https://www.consul.io/api-docs/agent/service
    https://www.consul.io/api-docs/agent/servicehttps://www.consul.io/api-docs/agent/check
    :param ip:
    :param name:
    :param port:
    :param method:
    :return:
    """
    headers = {
        'Content-Type': 'application/json'
    }
    grpc = {
        "GRPC": f'{ip}:{port}',
        "GRPCUseTLS": False,
        "Timeout": "5s",
        "Interval": "5s",
        "Http": "http://192.168.12.56:8866/health/check",
        # "DeregisterCriticalServiceAfter": "5s",
    }
    # {'tcp': '127.0.0.1:5000', 'interval': '5s', 'timeout': '30s', 'DeregisterCriticalServiceAfter': '30s'}
    http = {
        # "Id": f"{uuid1()}",
        # "Name": name,
        # "Http": "http://192.168.12.56:8866/health/check",
        'tcp': '192.168.12.126:8118',
        "DeregisterCriticalServiceAfter": "5s",
        # "Args": ["/usr/local/bin/check_redis.py"],
        "Interval": "5s",
        "Timeout": "5s"
    }
    body = {
        "ID": f"{uuid1()}",
        "Name": name,
        "Tags": ["primary", "v1"],
        "Address": ip,
        "Port": port,
        # "EnableTagOverride": False,
        "Check": None,
        # "Weights": {
        #     "Passing": 10,
        #     "Warning": 1
        # }
    }
    url = 'http://192.168.12.126:8500/v1/agent/service/register'

    if method == 'http':
        body.update({'Check': http})
    else:
        body.update({'Check': grpc})

    print(body)
    code = requests.put(url, json=body, headers=headers).status_code
    if code == 200:
        print('success')
    else:
        print('fail')


def consul_deregister(ip, port):
    """
    取消的是name
    :param ip:
    :param name
    :param port
    :return:
    """
    url = f'http://192.168.12.126:8500/v1/agent/service/deregister/{ip}:{port}'
    code = requests.put(url).status_code
    if code == 200:
        print('success')
    else:
        print('fail')


def fetch_consul_info():
    """
    获取服务使用
    :return:
    """
    payload = {'name': 'test-service', 'address': '127.0.0.1', 'port': 5000,
               'check': {'tcp': '127.0.0.1:5000', 'interval': '5s', 'timeout': '30s',
                         'DeregisterCriticalServiceAfter': '30s'}}

    import consul

    # print(consul.Check().tcp('127.0.0.1', 5000, '5s', '30s', '30s'))
    # 初始化 Consul 服务
    # return
    cursor = consul.Consul(host='192.168.12.126', port=8500)

    # 注册服务到 Consul
    cursor.agent.service.register(
        name='test-service', address='192.168.12.56', port=8866,
        # 心跳检查：间隔：5s，超时：30s，注销：30s
        check=consul.Check().tcp('127.0.0.1', 8866, '5s', '30s', '30s')
    )

    # 获取服务状态
    checks = cursor.agent.checks()
    status = checks.get('service:test-service').get('Status')
    print(status)

    # 获取服务
    services = cursor.agent.services()
    service = '%s:%s' % (services.get('test-service').get('Address'), services.get('test-service').get('Port'))
    print(service)

    # 添加 kv 数据
    result = cursor.kv.put('key', 'test-value')
    print(result)

    # 获取 kv 数据
    _, result = cursor.kv.get('key')
    result = result.get('Value').decode('utf-8')
    print(result)


if __name__ == '__main__':
    # http://s-yanshentiku.cdn.ixunke.com/qimg_optionsofid30089No4.jpeg
    # get_chrome_driver()
    # email_fetch()
    # freeze_support()
    # nacos_config_fetch()
    # nacos_register_instance('task-api-2', '192.168.12.56', 8866, 57890, grpc=True, ephemeral=False)
    # http://192.168.12.56:32226/actuator/health
    # http://192.168.12.56:8866/
    # consul_register("all-api-test", '192.168.12.56', 32226, 'http')
    # consul_register("http", '192.168.12.56', 57890, 'http')
    nacos_deregster_instance('gateway', '192.168.12.56', 49575)
    # fetch_consul_info()
    # consul_deregister('192.168.12.56', 57890)
    # consul_deregister('192.168.12.126', 32226)
