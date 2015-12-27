#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

from request import Request, Response
import os, sys, builtins
from config import Configuration

request = Request(os.environ['QUERY_STRING'], sys.stdin.read())
#request = Request('WF_PAGE=test.py&name=x', 'word=10')
response = Response()
config = Configuration('../aelfi.conf')

pageloc = '../' + request.args.pop('WF_PAGE')

error = False
if '.' not in pageloc.split('/')[-1]:
    if pageloc[-1] != '/':
        pageloc += '/'
    for index in config.indecies:
        if os.path.isfile(pageloc + index):
            pageloc += index
            break
    else:
        ext, request.page = config.errorresponses.get(404, ('txt', 'Error 404'))
        error = True

if not error and config.isprotected(pageloc):
    ext, request.page = config.errorresponses.get(403, ('txt', 'Error 403'))
    error = True

if not error:
    try:
        with open(pageloc) as file:
            request.page = file.read()
            request.pageloc = pageloc
            ext = pageloc.split('.')[-1]
            
    except IOError:
        ext, request.page = config.errorresponses.get(404, ('txt', 'Error 404'))
        error = True

# Why IO Error above
if ext == 'py':
    builtins.request, builtins.response = request, response
    import env
else:
    print('Content-Type:', 
          config.extensions.get(ext, 'text/text') + ';' + config.charset + '\n')
    print(request.page)
