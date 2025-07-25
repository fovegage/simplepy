import warnings

import pandas as pd
import pymongo
import pymysql
import redis

from simplepy import logger
from simplepy.config import MONGO_HOST, MONGO_PORT, MONGO_PWD, MONGO_AUTH_DB, MONGO_USER
from simplepy.config import MYSQL_USER, MYSQL_HOST, MYSQL_PWD, MYSQL_PORT
from simplepy.config import REDIS_HOST, REDIS_PWD, REDIS_PORT, REDIS_DB

warnings.filterwarnings("ignore")


class VpnBookMongo:

    def __init__(self, db, table):
        client = pymongo.MongoClient(host=MONGO_HOST, maxPoolSize=100, port=MONGO_PORT)
        client[MONGO_AUTH_DB].authenticate(name=MONGO_USER, password=MONGO_PWD)
        self.db = db
        self.table = table
        self.mongo_db = client[self.db][self.table]

    def repeat(self):
        """
        dsl去重
        :return:
        """
        pipeline = [
            {'$group': {
                '_id': {'disk_id': '$disk_id'},
                'uniqueIds': {'$addToSet': '$_id'},
                'count': {'$sum': 1}
            }},
            {'$match': {
                'count': {'$gt': 1}
            }}
        ]
        result = self.mongo_db.aggregate(
            pipeline
        )
        for item in result:
            logger.info(item)

    def pandas(self):
        """
        pandas去重
        :return:
        """
        df = pd.DataFrame(self.mongo_db.find())
        logger.info(df.shape)
        df = df.drop_duplicates(subset=['disk_id'])
        logger.info(df.shape)

    def insert(self, doc):
        self.mongo_db.insert_one(doc)

    def update_or_insert(self, find: dict, doc: dict):
        """
        插入数据
        Args:
            find:
            doc:

        Returns:

        """
        result = self.mongo_db.find_one_and_update(find, {"$set": doc})
        if not result:
            self.insert(doc)


class VpnBookRedis:
    def __init__(self):
        self.conn_pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PWD)

    @property
    def redis_client(self):
        return redis.Redis(connection_pool=self.conn_pool)

    def proxy(self, socks5=False):
        if socks5:
            proxies = {
                "http": f"socks5://{self.redis_client.get('temp_ip').decode()}",
                "https": f"socks5://{self.redis_client.get('temp_ip').decode()}"
            }
            return proxies
        proxies = {
            "http": self.redis_client.get('temp_ip').decode(),
            "https": self.redis_client.get('temp_ip').decode()
        }
        return proxies


def get_redis_pool():
    """
    redis 连接池
    :return:
    """
    conn_pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PWD)
    redis_pool = redis.Redis(connection_pool=conn_pool)
    return redis_pool


def redis_pub_sub_example():
    """
    pub example
    :return:
    """
    rd = VpnBookRedis()
    p = rd.redis_client.pubsub()
    p.subscribe('upanso')
    logger.info('连接成功')
    for msg in p.listen():
        if msg.get('type') == 'message':
            data = msg.get('data').decode()
            logger.info(data)


def get_mysql_conn(db):
    """
    mysql连接connect
    :param db:
    :return:
    """
    return pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        passwd=MYSQL_PWD,
        db=db,
        port=MYSQL_PORT,
        charset='utf8mb4'
    )


if __name__ == '__main__':
    redis_pub_sub_example()
