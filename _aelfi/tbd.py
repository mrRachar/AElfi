#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

import os, sys                      # To change working directory, to edit the python import path
import builtins                     # To transfer request, response to templates

from config import Configuration
from request import Request, Response

config = Configuration('config.json')    # Load in the configurations

# Create the main page loading variables
request = Request(os.environ['QUERY_STRING'], sys.stdin)        # The request, based of the query string (GET) and stdin (POST)
response = Response()                                           # Create an empty response file, for the page to fill in

# Handle the page location
request.location = request.args['AELFI_TBD_PAGE']               # Set the request file location to what is given
request.pageloc = '../' + request.args.pop('AELFI_TBD_PAGE')    # Store the file location for use in script, removing it from the GET vars passed to page

# Set up the main built in values
display = {             # A dict which will be passed to mako later, containing `request` and `response` by default for ease-of-use
            'request': request,
            'response': response
          }

for get in (request.args, request.get, request.plus_args, request.plus_get):
    if 'AELFI_TBD_PAGE' in get:
        get.pop('AELFI_TBD_PAGE')
    if 'AELFI_PAGE' in get:
        get.pop('AELFI_PAGE')

# To make these variables accessible in the templates
builtins.request, builtins.response = request, response

print = response.print  # To replace `print`'s functionality, so it can also handle auto header sending
sys.path.insert(0, './')                            # Allow files to be imported from the directory the file is going to be run in
sys.path.insert(1, os.path.abspath('./modules'))    # Allow files to be imported from the aelfi_modules

try:
    if os.path.isfile(request.pageloc):                                        # If the template is a file,
        with open(request.pageloc, encoding=config.charset) as templatefile:   #  open it and,
            response.page = templatefile.read()                                #  read the contents of the file, saving it as the page contents
            #aelfi_dir = os.getcwd()
            abs_pageloc = os.path.abspath(request.pageloc)
            #os.chdir(os.path.dirname(request.pageloc))
            # By providing the path to the template_module, the cwd should be changed anyway
            rendering = config.template_module.render(
                response.page,
                os.path.abspath('../'),
                display,
                abs_pageloc
                )  #  print it rendered with their template engine choice (default mako)
            # If the script didn't already, see if we can send the headers again,
            response.sendheader()   #  but leave til now 'cause rendering may change them, if the script doesn't print
            # Print the rendering
            print(rendering)
    else:
        response.status = 404, "File Not Found"
        response.sendheader()       # Make sure headers are away
        print('Error 404: AElfi was given a file which could not be found')
except BaseException as e:
    response.senderror(e)       # Let the response handle it, which will raise Error 500
