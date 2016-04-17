#!usr/bin/env python3
#-*- coding: UTF-8 -*-
import os, sys
from collections import OrderedDict as odict
from http import cookies
from config import Configuration
from agent import Agent
from urllib import parse

config = Configuration('../aelfi.conf')


# Request Section #

class Request:
    
    def __init__(self, get: str, post: str, *, pageloc: str=''):
        #(UN)QUOTE GET arguments
        self.q_args = odict((parse.unquote(arg.split('=')[0]), parse.unquote(arg.split('=')[1]))
                  for arg in get.split('&') if len(arg.split("=")) != 1)
        #(UN)QUOTE GET keywords
        self.q_keywords = [parse.unquote(arg) for arg in get.split('&') if '=' not in arg]
        #(UN)QUOTE POST all
        self.q_fields = odict((parse.unquote(arg.split('=')[0]), parse.unquote(arg.split('=')[1]) if len(arg.split('=')) > 1 else None)
                            for arg in post.split('&') if arg.split('=')[0] != '')

        # RAW GET arguments
        self.raw_args = odict((arg.split('=')[0], arg.split('=')[1])
                  for arg in get.split('&') if len(arg.split("=")) != 1)
        # RAW GET keywords
        self.raw_keywords = [arg for arg in get.split('&') if '=' not in arg]
        # RAW POST all
        self.raw_fields = odict((arg.split('=')[0], arg.split('=')[1] if len(arg.split('=')) > 1 else None)
                            for arg in post.split('&') if arg.split('=')[0] != '')

        # + PLUS GET arguments
        self.plus_args = odict((parse.unquote_plus(arg.split('=')[0]), parse.unquote_plus(arg.split('=')[1]))
                  for arg in get.split('&') if len(arg.split("=")) != 1)
        # + PLUS GET keywords
        self.plus_keywords = [parse.unquote_plus(arg) for arg in get.split('&') if '=' not in arg]
        # + PLUS POST all
        self.plus_fields = odict((parse.unquote_plus(arg.split('=')[0]), parse.unquote_plus(arg.split('=')[1]) if len(arg.split('=')) > 1 else None)
                            for arg in post.split('&') if arg.split('=')[0] != '')

        # Default GET arguments
        self.args = self.q_args
        # Default GET keywords
        self.keywords = self.q_keywords
        # Default POST all
        self.fields = self.plus_fields

        self.header = {
            'user agent': os.environ['HTTP_USER_AGENT'],
            'ip': os.environ['REMOTE_ADDR'],
            'server': os.environ['SERVER_NAME'],
            'protocol': os.environ['SERVER_PROTOCOL'],
            'connection type': os.environ.get('HTTP_CONNECTION', ''),
            'method': os.environ['REQUEST_METHOD'],
            'accepted language': os.environ['HTTP_ACCEPT_LANGUAGE'],
            'location': os.environ['REQUEST_URI'],
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
    def q_get(self) -> dict:
        get = odict((k, v) for k, v in self.q_args.items())
        get.update((k, None) for k in self.q_keywords)
        return get

    @property
    def q_post(self) -> dict:
        return odict((k, v) for k, v in self.q_fields.items())

    @property
    def raw_get(self) -> dict:
        get = odict((k, v) for k, v in self.raw_args.items())
        get.update((k, None) for k in self.raw_keywords)
        return get

    @property
    def raw_post(self) -> dict:
        return odict((k, v) for k, v in self.raw_fields.items())

    @property
    def plus_get(self) -> dict:
        get = odict((k, v) for k, v in self.plus_args.items())
        get.update((k, None) for k in self.plus_keywords)
        return get

    @property
    def plus_post(self) -> dict:
        return odict((k, v) for k, v in self.plus_fields.items())


    @property
    def cookies(self) -> cookies.SimpleCookie:
        return self.__cookies

    @property
    def directory(self) -> str:
        return '/'.join(self.pageloc.split('/')[:-1]) + '/'

    def __getitem__(self, headerkey: str):
        return self.header[headerkey]


# Response Section #

class Status:
    __code = 0
    __message = ''

    def __init__(self, code: int, message: str=''):
        if not isinstance(code, int):
            raise TypeError("The status code must be integer")
        self.__code = code
        self.__message = message

    @property
    def message(self) -> str:
        return self.__message

    @property
    def code(self) -> int:
        return self.__code

    def __str__(self) -> str:
        return str(self.code) + (' ' + self.message if self.message else '')


class Response:
    __status = Status(200)
    Status = Status

    def __init__(self, page: str=''):
        self.headersent = False
        self.header = {
            'Content-Type': 'text/html;charset=' + config.charset + ';',
        }
        self.__cookies = cookies.SimpleCookie()
        self.page = page

    def __getitem__(self, key: str):
        """Get the value stored by the key in the response's header
        :param item: str: the header key to access
        :return: the current values stored therewith
        """
        return self.header[key]

    def __setitem__(self, key: str, value):
        """Set the value with a key in the responses's header
        :param key: str: the header to store it under
        :param value: the value to store with the key
        """
        self.header[key] = value

    @property
    def status(self) -> Status:
        return self.__status

    @status.setter
    def status(self, value):
        """This will set the status. If the value is a Status object, it will be set directly.
        If it is an iterable of length 1 or 2, then it will set the first value to the code,
        and the second to the message

        :param value: Union[Status, Iterable]: the value for the status
        """
        if isinstance(value, Status):
            self.__status = value
        else:
            try:
                if 1 <= len(value) <= 2:
                    self.__status = Status(*value)
                else:
                    raise ValueError("Value must be of length 1 or 2")
            except TypeError:
                raise TypeError("Value must be Status or iterable of length 1 or 2, with the first element an integer")

    def sendheader(self):
        if self.headersent:
            return
        print('\n'.join('{}: {}'.format(k, v) for k, v in
                                                self.header.items()))
        print('Status Code: {!s}'.format(self.__status))
        if self.cookies:
            print(self.cookies)

        self.headersent = True
        print()
        sys.stdout.flush()

    @property
    def cookies(self) -> cookies.SimpleCookie:
        return self.__cookies

    def write(self, text: bytes):
        """Write a bytes stream to the page"""
        if not self.headersent:
            self.sendheader()
        sys.stdout.buffer.write(text)
        sys.stdout.flush()

    def print(self, *values, sep=' ', end='\n'):
        if not self.headersent:
            self.sendheader()
        sys.stdout.buffer.write(str(sep).encode(config.charset).join(str(value).encode(config.charset) for value in values)
                                + str(end).encode(config.charset))
        sys.stdout.flush()

    def refresh(self, time=0):
        self['Refresh'] = '{}'.format(time)
        self.print()
        self.close()

    def redirect(self, url, time=0):
        self['Refresh'] = '{};url={}'.format(time, url)
        self.print()
        self.close()

    def close(self):
        self.print('<!--')
        sys.exit()
        
