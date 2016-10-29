*The new AElfi build system differs from that of previous versions greatly. If you have used previous versions, please refesh your knowledge!*

## AElfi Build Files

Every AElfi application has an `aelfi.build` file in its root directory. This file allows you to customise how AElfi is set up, *(when `aelfi 
project build`  or `python3 _aelfi/build.py` is run)*, and how it's run, from what charset and templating engine is used, to creating routes which 
all the uri the user entered to be changed locally to something easier. AElfi build files have a special configuration language which is designed 
to make them easy to read and look nice.

*Build files may be left empty, putting stuff in them is completely optional*

**_Scroll down to see an nice example!_**

### Use

Use declarations make it possible to configure how AElfi operates. *For those used to the older system, these practically replace runtime configs*

*[Find out more about `use` declarations](use.md)*

### Include

Include declarations allow for libraries to be added to the sys.path so they're accessible from any file in your applications

*[Find out more about `use` declarations](include.md)*

### Routes

Routes, the most important part of build files, allow incoming uris to rerouted to another file to be handled. They also allow files to be protected,
forbidden, or to pretend there is nothing there, as well as setting up error documents.

*[Find out more about routes](routes.md)*
 
*Here's an example I made earlier, in traditional Blue-Peter style, to explain things better*
```AElfiBuild
# Comments can start with a # like in Python, or use /* */ to span multiple lines

# Use declarations allow you to set what AElfi uses. They are all optional
# Charset default is uft8
use charset utf16
# Template defaults to mako. To use others, see templating docs
use template jinja2

# Libraries allow you to provide folders,
#  whose contents (Python files) are importable from across your project
include <models>
include <extensions/main>

# Routes are the most important part of build files;
#  they let you reroute incoming requests,
#  which allows neater uris for the user!
# Reroute for products. language is a built in variable whose value is the HTTP ACCEPT LANGUAGE header
<product.py?id={id}&l={language}> <- <product/{id:[a-zA-Z0-9][a-zA-Z0-9]}>
# They also allow you to set up error documents
<errors/500.py> <- error
```