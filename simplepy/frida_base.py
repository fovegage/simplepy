import os
import sys

import frida
from flask import views
from loguru import logger

from simplepy.decorators import get_callback_path
from simplepy.utils import read_content


class FridaPkg:
    """
    frida基类mixin
    """
    package = None
    remote = None
    js_code = 'hook.js'
    server = False


class FridaBase(FridaPkg, views.MethodView):
    def __init__(self, spawn=True, demon=True, front=False):
        # app 启动前注入 spawn=False 则进行 attach
        self.spawn = spawn
        # 是否持续输出
        self.demon = demon
        # 连接手机
        if self.remote:
            # 不传默认usb，如果传入则格式为 192.168.12.92:4569
            manager = frida.get_device_manager()
            self.device = manager.add_remote_device(self.remote)
        else:
            self.device = frida.get_usb_device(timeout=60)
        # 最前台应用 将屏蔽基类中的package，替换为前台应用
        if front:
            self.package = self.device.get_frontmost_application().pid
            self.spawn = False
        # 启动app
        self.session = self.hack()
        # 脚本导出
        self.script = None

    def on_message(self, message, data):
        """
        rpc消息接收
        Args:
            message:
            data:

        Returns:

        """
        logger.info(data)
        if message["type"] == "send":
            logger.info("[+] {}".format(message["payload"]))
        else:
            logger.info("[-] {}".format(message))

    def hack(self):
        """
        启动app
        使用spawn和resume  先挂起，在恢复
        attach 直接对应用进行附加
        Returns:

        """
        if self.spawn:
            pid = self.device.spawn(self.package)
            session = self.device.attach(pid)
            self.device.resume(pid)
        else:
            session = self.device.attach(self.package)
        return session

    @get_callback_path
    def inject_script(self, **kwargs):
        """
        注入js, 以便进行rpc调用
        Args:
            **kwargs:

        Returns:

        """
        path = kwargs.get('path')
        full_path = os.path.join(path, self.js_code)
        js = read_content(full_path)
        script = self.session.create_script(js)
        script.on("message", self.on_message)
        script.load()
        # 持续输出
        if self.demon:
            sys.stdin.read()
        else:
            # function_name = kwargs.get('f_name')
            self.script = script.exports
            print(self.script)

    def start_server(self):
        """
        可以选择 flask 或者 fastapi
        子类必须实现
        Returns:

        """
