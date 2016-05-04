import builtins                     # The builtins, including request and response objects
import os, sys                      # To change working director, to edit the python import path
from config import Configuration    # For the encoding to open the file with

config = Configuration('../aelfi.conf') # Load in the configurations

# Set up the main built in values
request = builtins.request
response = builtins.response
display = {             # A dict which will be passed to mako later, containing `request` and `response` by default for ease-of-use
            'request': builtins.request,
            'response': builtins.response,
          }
print = response.print  # To replace `print`'s functionality, so it can also handle auto header sending

aelfi_directory = os.getcwd()
os.chdir(builtins.request.directory)                # Change the directory to the location of the document, so to allow it to act normal
sys.path.insert(0, './')                            # Allow files to be imported from the directory the file is going to be run in
sys.path.insert(1, aelfi_directory + '/modules')    # Allow files to be imported from the directory the file is going to be run in

exec(builtins.response.page)    # Run the script

# Make a found function, so as to allow for better slicing
found = lambda x: x if x is not -1 else None
finaldot = builtins.request.pageloc.rfind('.')  # Get the location of the final dot of the file: 'xyz . py'
os.chdir(aelfi_directory)   #Go back to the AElfi directory, as paths will be relative to here

# Get the location of where the template could be,
#  use the found function to convert `-1`s to None, so to not cut if no '.' found
templatelocation = builtins.request.pageloc[:found(builtins.request.pageloc.rfind('.'))] + '.view'
if os.path.isfile(templatelocation):                                        # If the template is a file,
    with open(templatelocation, encoding=config.charset) as templatefile:   #  open it and,
        rendering = config.template_module.render(
            templatefile.read(),
            os.path.abspath('../'),
            display,
            os.path.abspath(templatelocation)
            )  #  print it rendered with their template engine choice (default mako)
        # If the script didn't already, see if we can send the headers again,
        response.sendheader() #  but leave til now 'cause rendering may change them, if the script doesn't print
        # Print the rendering
        print(rendering)
