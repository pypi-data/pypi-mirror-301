#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import pickle
import requests
from gsoft_py_utils.login.douban_login import douban


'''基类客户端'''
class BaseClient():
    def __init__(self, website_name=None, reload_history=True, auto_cache_history=True, history_path=None, **kwargs):
        self.supported_apis = {
            'douban': douban().login
        }
        assert website_name in self.supported_apis
        self.rootdir = history_path
        if not self.rootdir:
            self.rootdir = os.getcwd()
        self.website_name = website_name
        self.reload_history = reload_history
        self.auto_cache_history = auto_cache_history
        self.infos_return, self.session = {}, requests.Session()
    '''模拟登录'''
    def login(self, username='none', password='none', mode='pc', crack_captcha_func=None, **kwargs):
        need_new_login = True
        if self.reload_history:
            self.infos_return, self.session, need_new_login = self.loadhistory(username)
        if need_new_login:
            api = self.supported_apis[self.website_name]
            self.infos_return, self.session = api(username, password, mode, crack_captcha_func, **kwargs)
        else:
            print(f"[INFO]: Resume {username}'s session and infos from {os.path.join(self.rootdir, self.website_name+'.pkl')}")
        if self.auto_cache_history: self.savehistory(username, self.infos_return, self.session)
        return self.infos_return, self.session
    '''保存历史数据'''
    def savehistory(self, username, infos_return, session):
        history_path = os.path.join(self.rootdir, self.website_name+'.pkl')
        history_infos = {}
        if os.path.exists(history_path):
            fp = open(history_path, 'rb')
            history_infos = pickle.load(fp)
            fp.close()
        history_infos[username] = [infos_return, session]
        fp = open(history_path, 'wb')
        pickle.dump(history_infos, fp)
        fp.close()
    '''导入历史数据'''
    def loadhistory(self, username):
        history_path = os.path.join(self.rootdir, self.website_name+'.pkl')
        # 不存在历史文件
        if not os.path.exists(history_path): return None, None, True
        # 读取history文件
        fp = open(history_path, 'rb')
        history_infos = pickle.load(fp)
        fp.close()
        # 如果username不存在
        if username not in history_infos: return None, None, True
        # 提取对应的数据
        infos_return, session = history_infos[username]
        # 检查是否已经过期
        try:
            if self.checksessionstatus(session, infos_return):
                return None, None, True
        except:
            return None, None, True
        # 返回可用的数据
        return infos_return, session, False
    '''检查会话是否已经过期, 过期返回True'''
    def checksessionstatus(self, session, infos_return):
        return True
