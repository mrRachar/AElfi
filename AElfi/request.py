#!usr/bin/env python3
#-*- coding: UTF-8 -*-
import os, sys
from collections import OrderedDict as odict
from http import cookies
from config import Configuration
from agent import Agent

config = Configuration('../aelfi.conf')

class Request:
    
    def __init__(self, get: str, post: str, *, pageloc: str=''):
        #GET arguments
        self.args = odict((arg.split('=')[0], arg.split('=')[1])
                  for arg in get.split('&') if len(arg.split("=")) != 1)
        #GET keywords
        self.keywords = [arg for arg in get.split('&') if '=' not in arg]
        #POST all
        self.fields = odict((arg.split('=')[0], arg.split('=')[1] if len(arg.split('=')) > 1 else None)
                            for arg in post.split('&') if arg.split('=')[0] != '')
        self.header = {
            'user agent': os.environ['HTTP_USER_AGENT'],
            'ip': os.environ['REMOTE_ADDR'],
            'server': os.environ['SERVER_NAME'],
            'protocol': os.environ['SERVER_PROTOCOL'],
            'connection type': os.environ['HTTP_CONNECTION'],
            'method': os.environ['REQUEST_METHOD'],
            'accepted language': os.environ['HTTP_ACCEPT_LANGUAGE'],
        }
        self.agent = Agent(self.header['user agent'])
        self.__cookies = cookies.SimpleCookie()
        if 'HTTP_COOKIE' in os.environ:
            self.__cookies.load(os.environ['HTTP_COOKIE'])
        self.pageloc = pageloc
        self.location = ''
        
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
    def __init__(self, page: str=''):
        self.headersent = False
        self.header = {
            'Content-Type': 'text/html;charset=' + config.charset + ';',
        }
        self.__cookies = cookies.SimpleCookie()
        self.page = page

    def sendheader(self):
        if self.headersent:
            return
        print('\n'.join('{}: {}'.format(k, v) for k, v in
                                                self.header.items()))
        if self.cookies:
            print(self.cookies)
        self.headersent = True
        print()
        sys.stdout.flush()

    @property
    def cookies(self) -> cookies.SimpleCookie:
        return self.__cookies

    def print(self, *values, sep=' ', end='\n'):
        if not self.headersent:
            self.sendheader()
        sys.stdout.buffer.write(str(sep).encode(config.charset).join(str(value).encode(config.charset) for value in values)
                                + str(end).encode(config.charset))
        sys.stdout.flush()
    
        
