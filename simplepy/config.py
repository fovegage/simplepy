from environs import Env

env = Env()
# TODO: nacos 配置注册中心
# env.read_env('/Users/gaozhe/PycharmProjects/codeline/libs/simplepy_online.env')

# redis
REDIS_HOST = env.str('REDIS_HOST', '')
REDIS_PORT = env.int('REDIS_PORT', 6379)
REDIS_PWD = env.str('REDIS_PWD', None)
REDIS_DB = env.int('REDIS_DB', 1)

# mysql
MYSQL_HOST = env.str('MYSQL_HOST', '')
MYSQL_USER = env.str('MYSQL_USER', '')
MYSQL_PWD = env.str('MYSQL_PWD', None)
MYSQL_PORT = env.int('MYSQL_PORT', 3306)

# mongo
MONGO_HOST = env.str('MONGO_HOST', '')
MONGO_PORT = env.int('MONGO_PORT', 27017)
MONGO_USER = env.str('MONGO_USER', '')
MONGO_PWD = env.str('MONGO_PWD', None)
MONGO_AUTH_DB = env.str('MONGO_AUTH_DB', '')

# email
EMAIL_USER = env.str('EMAIL_USER', None)
EMAIL_PWD = env.str('EMAIL_PWD', None)

# proxy
PROXY_HOST = env.str('PROXY_HOST', '')
PROXY_PORT = env.int('PROXY_PORT', 0)
PROXY_USER = env.str('PROXY_USER', '')
PROXY_PWD = env.str('PROXY_PWD', None)

# redis 账户池
ACCOUNT_POOL_API = env.str('ACCOUNT_POOL_API', '')

# 阿里云oss
