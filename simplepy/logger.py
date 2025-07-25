import time
from pathlib import Path

from loguru import logger

project_path = Path.cwd()
log_path = Path(project_path, "logs")
t = time.strftime("%Y_%m_%d")


class Logger:
    __instance = None
    logger.add(f"{log_path}/crawl_log_{t}.log", rotation="500MB", encoding="utf-8", enqueue=True,
               retention="7 days", level='ERROR')

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Logger, cls).__new__(cls, *args, **kwargs)

        return cls.__instance

    @staticmethod
    def join_msg(msgs):
        return '\t'.join([str(x) for x in msgs])

    def info(self, *msg):
        return logger.info(self.join_msg(msg))

    def debug(self, *msg):
        return logger.debug(self.join_msg(msg))

    def warning(self, *msg):
        return logger.warning(self.join_msg(msg))

    def error(self, *msg):
        return logger.error(self.join_msg(msg))


if __name__ == '__main__':
    log = Logger()
    log.info("中文test", "sss")
    log.debug("中文test")
    log.warning("中文test")
    log.error("中文test")
