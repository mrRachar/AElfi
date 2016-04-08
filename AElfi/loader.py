#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

from request import Request, Response
import os, sys, builtins

# Create the main page loading variables
request = Request(os.environ['QUERY_STRING'], sys.stdin.read()) # The request, based of the query string (GET) and stdin.read (POST)
response = Response()                                           # Create an empty response file, for the page to fill in

# Handle the page location
request.location = request.args['AELFI_PAGE']           # Set the request file location to what is given
request.pageloc = '../' + request.args.pop('AELFI_PAGE')  # Store the file location for use in script, removing it from the GET vars passed to page


try:                                            # Try to,
    with open(request.pageloc, 'rb') as file:   #  open the python file
        response.page = file.read()                 # Read the contents of the file, saving it as the page contents
except IOError as e:            # Treat can't find file as 404, hope redirect will happen
    response.status = 404, "File Not Found"
    response.sendheader()       # Make sure headers are away
    print()                     # Print a clear line to separate the error trace
    print('', e, e.__traceback__, sep='<br/>\n') #Print the error and the traceback

# Set the builtins, to be transferred to the environment
builtins.request, builtins.response = request, response
try:                # Try to:
    import env      #  execute the script
except BaseException as e:      # Treat as Internal Server Error
    response.status = 500, "Internal Server Error"
    response.sendheader()       # Make sure headers are away
    print()                     # Print a clear line to separate the error trace
    print('Error:', e, e.__traceback__, end='<br/>\n') # Print the error and the traceback



# vv OLD NOT NEEDED CODE vv ##
'''error = False
if '.' not in file_location.split('/')[-1]:
    if file_location[-1] != '/':
        file_location += '/'
    if os.path.isfile(file_location + 'index.py'):
        file_location += 'index.py'
    else:
        ext, response.page = config.errorresponses.get(404, ('txt', 'Error 404'))
        error = 404
'''
# ^^ OLD NOT NEEDED CODE ^^ ##
