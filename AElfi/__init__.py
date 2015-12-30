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
    for index in config.indecies:
        if os.path.isfile(pageloc + index):
            pageloc += index
            break
    else:
        ext, response.page = config.errorresponses.get(404, ('txt', 'Error 404'))
        error = True

if not error and config.isprotected(pageloc):
    ext, response.page = config.errorresponses.get(403, ('txt', 'Error 403'))
    error = True

if not error:
    try:
        with open(pageloc, 'rb') as file:
            response.page = file.read()
            request.pageloc = pageloc
            ext = pageloc.split('.')[-1]
            
    except IOError:
        ext, response.page = config.errorresponses.get(404, ('txt', 'Error 404'))
        error = True

# Why IO Error above
if ext == 'py':
    builtins.request, builtins.response = request, response
    try:
        import env
    except:     #i.e. Internal Server Error
        ext, response.page = config.errorresponses.get(500, ('txt', 'Error 500'))
        error = True
        sys.stdout.flush()
        sys.stdout.buffer.write(response.page)
else:
    print('Content-Type:', 
          config.extensions.get(ext, config.defaultmime) + ';' + config.charset + '\n')
    sys.stdout.flush()
    sys.stdout.buffer.write(response.page)
