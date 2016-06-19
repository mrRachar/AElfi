#!usr/bin/env python3
#-*- coding: UTF-8 -*-
"""This stores the Request, Response and related classes, for their objects in the AElfi environment as part of the Connection Object Model

When your getting a page ready for the user, you are dealing with two parts: the user's request, and your response. Apache litters information about
    these in many different variables, from os.environ to sys.stdin, and doesn't give them in a very nice format. This can make your code hard to
    write, as you have to find everything, and scavenge the information from it once you have, and even harder to understand later.

AElfi, natrually, puts everything nice and neatly in two objects, one a Request instance, one a Response. These objects contain everything you need to
    work out exactly the what, how and who of the user, and to control exactly what you giving them back. They are both already in the global scope,
    so you've got them automatically.

Request - Request contains all the information that the user has sent. This includes any 'GET' or 'POST' variables, as well as cookies, protocol, ip,
    and requested URL, even the language their browser asked for. It also contains the user agent, which has been parsed.

Response - To control your response other then how the page looks like, you will need to use response. This contains the HTTP headers and any cookies
    you're sending back.
"""

import os, sys
import traceback, re, html                      # For error printing, and re for post file scraping aswell
import tempfile                                 # Use for getting uploaded files
from collections import OrderedDict as odict
from http import cookies
from config import Configuration
from agent import Agent
from urllib import parse

config = Configuration('../aelfi.conf')


# Request Section #

class UploadedFile:
    name = ''
    contenttype = ''
    file = None
    def __init__(self, name='', contenttype=''):
        self.name = name or self.name
        self.contenttype = contenttype or self.contenttype
        self.file = tempfile.TemporaryFile('w+b')

class Request:
    """The request object, request, allows you access to all the information the user has sent you. It is, like all COM objects, automatically available for you in the global scope.

    Anything in header can also be accessed by subscripting the request object, so request.header['ip'] and request['ip'] are the same.
    """

    def __init__(self, get: str, post, *, pageloc: str=''):
        """Set up the request using the given get string, post string, and page location."""
        post = post.buffer.read()

        #(UN)QUOTE GET arguments
        self.q_args = odict((parse.unquote(arg.split('=')[0]), parse.unquote(arg.split('=')[1]))
                  for arg in get.split('&') if len(arg.split("=")) != 1)
        #(UN)QUOTE GET keywords
        self.q_keywords = [parse.unquote(arg) for arg in get.split('&') if '=' not in arg]
        #(UN)QUOTE POST all
        self.q_fields = self.parse_post(post, parse.unquote)

        # RAW GET arguments
        self.raw_args = odict((arg.split('=')[0], arg.split('=')[1])
                  for arg in get.split('&') if len(arg.split("=")) != 1)
        # RAW GET keywords
        self.raw_keywords = [arg for arg in get.split('&') if '=' not in arg]
        # RAW POST all
        self.raw_fields = self.parse_post(post)

        # + PLUS GET arguments
        self.plus_args = odict((parse.unquote_plus(arg.split('=')[0]), parse.unquote_plus(arg.split('=')[1]))
                  for arg in get.split('&') if len(arg.split("=")) != 1)
        # + PLUS GET keywords
        self.plus_keywords = [parse.unquote_plus(arg) for arg in get.split('&') if '=' not in arg]
        # + PLUS POST all
        self.plus_fields = self.parse_post(post, parse.unquote_plus)

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
            'language': os.environ['HTTP_ACCEPT_LANGUAGE'].split(',')[0],
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
        """These are any get variables you have been sent, either in keywords or in args. They are in a OrderedDict, args first, and keywords have the
        value None. This is the same as q_get.

        For the request "index.py?name=hello&settings&page=4&advanced", get would be:
            OrderedDict({'name': 'hello', 'page': '4', 'settings':None, 'advanced': None}).
        *Also available with the plus_ and raw_ prefixes
        """


        get = odict((k, v) for k, v in self.args.items())
        get.update((k, None) for k in self.keywords)
        return get

    @property
    def post(self) -> dict:
        """These are all the POST variables that the client has sent you, if they have sent any, as key-value pairs, in the order they were sent in.
        This is the same as plus_post.

        *Also available with the q_ and raw_ prefixes
        """
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
        """Cookies is a http.cookies.SimpleCookies object with the cookies sent by the client.

        These are the cookies the client has sent to you, which should only be those for your site. See the Python documentation for more information
        on SimpleCookies objects.
        """
        return self.__cookies

    @property
    def directory(self) -> str:
        return '/'.join(self.pageloc.split('/')[:-1]) + '/'

    def __getitem__(self, headerkey: str):
        return self.header[headerkey]

    @staticmethod
    def parse_post(querystring, map_f=(lambda x: x)) -> odict:
        if os.environ.get('CONTENT_TYPE', '').startswith('multipart/form-data'):
            nextline = lambda string: string[string.index(b'\n')+1:]
            querystring = querystring.lstrip(b'\n\r \t')
            boundary = b'--' + re.match(rb'multipart/form-data;\s*boundary=(-+\w+)', os.environ['CONTENT_TYPE'].encode(config.charset)).group(1)
            post = odict()
            for arg in querystring.split(boundary)[1:-1]:
                arg = arg.lstrip(b'\n\r \t')
                name, filename = re.match(rb'(?:Content-Disposition:\s*form-data;\s*)?name=("[^"]+"|\'[^\']\')(?:; (?:filename=("[^"]+"|\'[^\']\'))?)?', arg).groups()
                arg = nextline(arg)
                if filename is None:
                    arg = nextline(arg)[:-1]
                    name = name.decode(config.charset)
                    post[name[1:-1]] = arg.decode(config.charset) if arg.decode(config.charset)[-1] != '\r' else arg.decode(config.charset)[:-1]
                    continue
                name, filename = name.decode(config.charset), filename.decode(config.charset)
                contenttype = re.match(rb'Content-Type:\s*([A-Za-z0-9/-_:]+)', arg).group(1).decode(config.charset)
                uploaded_file = UploadedFile(name=filename[1:-1], contenttype=contenttype)
                arg = nextline(nextline(arg))[:-1]
                uploaded_file.file.write(arg)
                uploaded_file.file.seek(0)
                post[name[1:-1]] = uploaded_file
            return post
        else:
            querystring = querystring.decode(config.charset)
            return odict((map_f(arg.split('=')[0]), map_f(arg.split('=')[1])
                if len(arg.split('=')) > 1
                else None)
            for arg in querystring.split('&') if arg.split('=')[0] != '')

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
        print('Status: {!s}'.format(self.__status))
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
        self.close()

    def redirect(self, url, time=0):
        self['Refresh'] = '{};url={}'.format(time, url)
        self.close()

    def close(self):
        self.print('<!--')
        sys.exit()

    def senderror(self, error):      # Treat as Internal Server Error
        self.status = 500, "Internal Server Error"
        self.sendheader()       # Make sure headers are away
        #self.print('raised {}:'.format(type(e).__name__), e, '<br/></br>', '<br/>'.join(traceback.format_tb(e.__traceback__)), end='<br/>\n') # Print the error and the traceback
        f_tb = traceback.format_tb(error.__traceback__)
        #self.print(f_tb)
        #self.print()
        self.print("""\
<html>
    <head>
        <title>Scripts Errors</title>
        <style>
            body {{
                font-family: sans-serif;
                text-align: center;
            }}
            div#t {{
                text-align: center;
            }}
            table {{
                border: none;
                display: inline-block;
            }}
            td {{
                text-align: left;
                margin: 0;
                padding: 3px;
            }}
            td:hover {{
                background: #eeeeee;
                font-weight: 600;
            }}
        </style>
    </head>
    <body>
        <h2>Internal Error Raised</h2>
        <p style="font-weight:bold">A {errortype} was raised in line {line}: <em>{message}</em></p>
        <table><tr><td>{quote}</td></tr></table>
        <h3>Traceback</h3>
        <div id='t'>
            <table>
                {traceback}
            </table>
        </div>
    </body>
</html>""".format(
            errortype = error.__class__.__name__,
            message = str(error),
            line = re.search(r'line (\d+)', f_tb[-1]).group(1) if re.search(r'line (\d+)', f_tb[-1]) else '(unknown)',
            quote = html.escape(f_tb[-1]).strip('\n \t'),
            traceback = "\n            ".join("<tr><td>{}</td></tr>".format(html.escape(part).strip('\n \t')) for part in f_tb[1:])
        ))
