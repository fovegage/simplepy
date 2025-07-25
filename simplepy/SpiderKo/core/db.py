import redis
from pymongo import MongoClient
from SpiderKo.config import *


class DbMixin:
    @staticmethod
    def redis_client():
        conn_pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_POSSWORD)
        return redis.Redis(connection_pool=conn_pool)

    @staticmethod
    def mongo_client():
        return MongoClient(host=MONGO_HOST, port=MONGO_PORT)

    @staticmethod
    def is_exist_by_mongo(db: str, table: str, key: str, value: str):
        """
        查询记录是否存在，返回True
        :param db:
        :param table: 数据库名称
        :param value:
        :param key:
        :return: True / False
        """
        mongo_db = DbMixin.mongo_client()[db]
        mongo_table = mongo_db[table]
        query = {key: value}
        mongo_doc = mongo_table.find(query).count()
        return True if mongo_doc > 0 else False

    @staticmethod
    def mysql_client():
        pass

    @staticmethod
    def es_client(self):
        pass


class ClientDb(DbMixin):
    def __init__(self, db, table):
        """

        :param db: mysql / mongo / es
        :param table:
        """
        self.db = db
        self.table = table
        # 外部进行单例模式
        self.m_client = self.mongo_client()
        self.r_client = self.redis_client()

    def create_or_query(self, *args, **kwargs):
        """
        clent = ClientDb('pans', 'upanso')
        clent.create_or_query(disk_id='1')
        :param kwargs:
        :return:
        """
        print(args, kwargs)
        # coll = db.pans.upanso
        # cursor = coll.count_documents({'disk_id': 'f90gGV8VDET3XBvtINsj4'})
        mongo_db = self.m_client[self.db]  # 库
        mongo_table = mongo_db[self.table]  # 表
        new_query = dict([args])
        mongo_doc = mongo_table.count_documents(new_query)

        if mongo_doc == 0 and len(kwargs) == 0:
            mongo_table.insert_one(new_query)

        if mongo_doc == 0 and len(kwargs) != 0:
            mongo_table.insert_one(kwargs)


if __name__ == '__main__':
    clent = ClientDb('pans', 'upanso1')
    a = {"name": "gage"}
    clent.create_or_query('disk_id', '111', **a)
