import os
import platform

from simplepy.config import env
from simplepy.logger import Logger

logger = Logger()
LIB_PATH = os.path.dirname(__file__)
ROOT_PATH = os.path.dirname(LIB_PATH)

IS_WINDOWS = True if platform.system() == 'Windows' else False
IS_LINUX = True if platform.system() == 'Linux' else False
IS_MAC = True if platform.system() == 'Darwin' else False


def init_db(path=''):
    if not os.path.isfile(path):
        logger.warning('请传递正确的环境变量路径')
    env.read_env(path)
