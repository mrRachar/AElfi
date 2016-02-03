import builtins                     # The builtins, including request and response objects
import os                           # To change working director
from mako import template           # For auto-templating
from .config import Configuration   # For the encoding to open the file with

config = Configuration('../aelfi.conf') # Load in the configurations

# Set up the main built in values
request = builtins.request
response = builtins.response
display = {}    # An empty dict which will be passed to mako later
print = response.print #To replace `print`'s functionality, so it can also handle auto header sending

aelfi_directory = os.getcwd()
os.chdir(builtins.request.directory)    #  change the directory to the location of the document, so to allow it to act normal

exec(builtins.response.page)    # Run the script

# If the script didn't already,
response.sendheader() # see if we can send the headers again

try:
    # Make a found function, so as to allow for better slicing
    found = lambda x: x if x is not -1 else None
    finaldot = builtins.request.pageloc.rfind('.')  # Get the location of the final dot of the file: 'xyz . py'
    os.chdir(aelfi_directory)   #Go back to the AElfi directory, as paths will be relative to here
    # Get the location of where the template could be,
    #  use the found function to convert `-1`s to None, so to not cut if no '.' found
    templatelocation = builtins.request.pageloc[:found(builtins.request.pageloc.rfind('.'))] + '.template'
    if os.path.isfile(templatelocation):                                        # If the template is a file,
        with open(templatelocation, encoding=config.charset) as templatefile:   #  open it and,
            print(template.Template(templatefile.read()).render(**display))     #  print it rendered with mako
except AttributeError:
    pass
