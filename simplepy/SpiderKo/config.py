"""
配置类
"""
import os

# 代理部分
AcceptLanguage = "zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6"

# PC Phone  管理类  自己管理 不适用 fake
UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"

headers = {
    "User-Agent": UserAgent,
    "Accept-Language": AcceptLanguage,
    "Host": None,
    "Origin": None
}
HEADERS = {key: value for key, value in headers.items() if value is not None}

# 数据库部分
REDIS_HOST = os.environ.get('REDIS_HOST', '49.65.124.203')
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_POSSWORD = os.environ.get('REDIS_PASSWORD', '416798GaoZhe!')

MONGO_HOST = "127.0.0.1"
MONGO_PORT = 27017
# 爬虫代理
