#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

from request import Request, Response
import os, sys, builtins, shutil
from config import Configuration

request = Request(os.environ['QUERY_STRING'], sys.stdin.read())
response = Response()
config = Configuration('../aelfi.conf')

request.location = request.args['AELFI_PAGE']
pageloc = '../' + request.args.pop('AELFI_PAGE')

error = False
if '.' not in pageloc.split('/')[-1]:
    if pageloc[-1] != '/':
        pageloc += '/'
    if os.path.isfile(pageloc + 'index.py'):
        pageloc += 'index.py'
    else:
        ext, response.page = config.errorresponses.get(404, ('txt', 'Error 404'))
        error = 404

if not error:
    try:
        with open(pageloc, 'rb') as file:
            response.page = file.read()
            request.pageloc = pageloc
            ext = pageloc.split('.')[-1]
            
    except IOError:
        ext, response.page = config.errorresponses.get(404, ('txt', 'Error 404'))
        error = 404

if error:
    response.header['Status'] = str(error)
    if ext != 'py':
        request.sendheader()
        print(response.page)

builtins.request, builtins.response = request, response
try:
    import env
except BaseException as e:     #i.e. Internal Server Error
    ext, response.page = config.errorresponses.get(500, ('txt', 'Error 500</br>' + str(e)))
    error = 500
    print()
    print(response.page)
