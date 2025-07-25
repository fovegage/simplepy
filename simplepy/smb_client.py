#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：codeline
@File    ：smb.py
@Author  ：fovegage
@Email   ：fovegage@gmail.com
@Date    ：2022/6/10 12:11
"""
import datetime
import os

import pandas as pd
from smb.SMBConnection import SMBConnection
from smb.smb_structs import OperationFailure


class SmbClient:
    def __init__(self, ip, username, password, server_name, port=445):
        """

        :param ip:
        :param username:
        :param password:
        :param server_name:
        :param port:
        """
        self.ip = ip
        self.username = username
        self.password = password
        self.port = port
        self.server_name = server_name
        self.server = self.connect()
        # self.file_list = self.file_list

    def connect(self):
        '''
        建立smb服务连接
        :param user_name:
        :param passwd:
        :param ip:
        :param port: 445或者139
        :return:
        '''
        samba = SMBConnection(self.username, self.password, '', '')
        samba.connect(self.ip, self.port)
        status = samba.auth_result
        if status:
            return samba
        else:
            raise Exception('connect fail')

    def file_list(self, dir_name):
        server = self.connect()
        for item in server.listPath(self.server_name, dir_name):
            if item.filename[0] != '.':
                print(item.filename)
                server.retrieveFile()
                print(pd.read_excel(item.filename))

        self.server.close()

    # def __enter__(self):
    #     return self
    #
    # def __exit__(self, *args):
    #     self.server.close()


if __name__ == '__main__':
    """
    https://blog.csdn.net/qq_43314560/article/details/113882498
    """

    ip = '192.168.12.153'
    username = 'admin'
    pwd = '416798gao'
    name = 'nas'
    sm = SmbClient(ip, username, pwd, name)
    # with sm.file_list(1) as op:
    #
    sm.file_list('/志祥/hn/result-xlsx/')
