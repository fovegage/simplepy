from snowflake.client import get_guid


def get_snow_id() -> int:
    """
    TODO: 单列实现 类封装
    开启服务：snowflake_start_server
    获取雪花ID
    单列模式  直接调用了包内的单列
    # 节点1
    snowflake_start_server --worker=1
    # 节点2
    snowflake_start_server --worker=2
    :return:
    """
    return get_guid()
