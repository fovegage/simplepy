# coding: utf-8
import pandas as pd
from simplepy.db import get_mysql_conn
from sqlalchemy import create_engine


def filter_by_date():
    """
    根据时间过滤数据
    :return:
    """


def filter_by_type():
    """
    根据指定类型过滤数据
    :return:
    """


def values_count():
    """
    统计某一列值对应的数量
    :return:
    """


def read_sql():
    """
    读取mysql
    index_col： 指定索引
    :return:
    """
    conn = get_mysql_conn('db')
    sql = 'select * from spider;'
    df = pd.read_sql(sql, conn, index_col='snow_id')
    print(df)


def read_json():
    """
    读取json
    :return:
    """


def store_to_sql(db_name, table, dataframe):
    """
    保存到MySQL
    :return:
    """
    conn = get_mysql_conn(db_name)
    engine = create_engine(conn, encoding='utf8')
    dataframe.to_sql(table, con=engine, if_exists='append', index=False)


def store_to_csv(df, path_name, mode='w', sep=','):
    """
    传递 含文件名的路径
    :param df:
    :param path_name:
    :param mode:
    :param sep:
    :return:
    """
    df.to_csv(path_name, encoding='utf-8-sig', mode=mode, sep=sep)


if __name__ == '__main__':
    read_sql()
