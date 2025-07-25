import os
import platform

LIB_PATH = os.path.dirname(__file__)
ROOT_PATH = os.path.dirname(LIB_PATH)

IS_WINDOWS = True if platform.system() == 'Windows' else False
IS_LINUX = True if platform.system() == 'Linux' else False
IS_MAC = True if platform.system() == 'Darwin' else False
