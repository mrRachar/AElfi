#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

from request import Request, Response
import os, sys, builtins, traceback

# Create the main page loading variables
request = Request(os.environ['QUERY_STRING'], sys.stdin)        # The request, based of the query string (GET) and stdin (POST)
response = Response()                                           # Create an empty response file, for the page to fill in

# Handle the page location
request.location = request.args['AELFI_PAGE']                       # Set the request file location to what is given
request._page_location = '../' + request.args.pop('AELFI_PAGE')     # Store the file location for use in script, removing it from the GET vars passed to page

for get in (request.args, request.get, request.plus_args, request.plus_get):
    try:
        get.pop('AELFI_PAGE')
    except KeyError:
        pass

try:                                                    # Try to,
    with open(request._page_location, 'rb') as file:    #  open the python file
        response.page = file.read()                     # Read the contents of the file, saving it as the page contents
except IOError as e:            # Treat can't find file as 404, hope redirect will happen
    response.status = 404, "File Not Found"
    response.sendheader()       # Make sure headers are away
    print('Error 404?:', e, '<br/></br>', '<br/>'.join(traceback.format_tb(e.__traceback__)), end='<br/>\n') # Print the error and the traceback

# Set the builtins, to be transferred to the environment
builtins.request, builtins.response = request, response
try:                # Try to:
    import env      #  execute the script
except BaseException as e:      # Treat as Internal Server Error
    response.senderror(e)       # Let the response handle it, which will raise Error 500
