#!usr/bin/env python3
#-*- coding: UTF-8 -*-
import os
from collections import OrderedDict as odict
from http import cookies

class Request:
    
    def __init__(self, get: str, post: str, *, page: str='', pageloc: str=''):
        self.args = odict((arg.split('=')[0], arg.split('=')[1])
                  for arg in get.split('&') if len(arg.split("=")) != 1)
        self.keywords = [arg for arg in get.split('&') if '=' not in arg]
        self.fields = odict((arg.split('=')[0], arg.split('=')[1] if len(arg.split('=')) > 1 else None)
                            for arg in post.split('&'))
        self.header = {
            'user agent': os.environ['HTTP_USER_AGENT'],
            #'ip': os.environ['REMOTE_ADDRESS'],
        }   
        self.__cookies = cookies.SimpleCookie()
        if 'HTTP_COOKIE' in os.environ:
            self.__cookies.load(os.environ['HTTP_COOKIE'])
        self.page = page
        self.pageloc = pageloc
        
    @property
    def get(self) -> dict:
        get = odict((k, v) for k, v in self.args.items())
        get.update((k, None) for k in self.keywords)
        return get

    @property
    def post(self) -> dict:
        return odict((k, v) for k, v in self.fields.items())

    @property
    def cookies(self) -> cookies.SimpleCookie:
        return self.__cookies

    @property
    def directory(self) -> str:
        return '/'.join(self.pageloc.split('/')[:-1]) + '/'


class Response:
    def __init__(self):
        self.headersent = False
        self.header = {
            'Content-Type': 'text/html;charset=utf-8',
        }
        self.__cookies = cookies.SimpleCookie()

    def sendheader(self):
        if self.headersent:
            return
        print('\n'.join('{}: {}'.format(k, v) for k, v in
                                                self.header.items()))
        if response.cookies:
            print(self.cookies)
        self.headersent = True
        print()

    @property
    def cookies(self) -> cookies.SimpleCookie:
        return self.__cookies

    def print(self, *values, **kwargs):
        if not self.headersent:
            self.sendheader()
        print(*values, **kwargs)
    
        
