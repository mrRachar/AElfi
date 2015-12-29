import builtins, os
from mako import template

request = builtins.request
response = builtins.response
display = {}
try:
    os.chdir(builtins.request.directory)
except AttributeError:
    pass
print = response.print

exec(builtins.request.page)

response.sendheader()

try:
    found = lambda x: x if x is not -1 else None
    finaldot = builtins.request.pageloc.rfind('.')
    #Start this 1 char in to miss the ../, instead get ./ (rel dir)
    templatelocation = builtins.request.pageloc[1:found(builtins.request.pageloc.rfind('.'))] + '.template'
    if os.path.isfile(templatelocation):
        with open(templatelocation, encoding='utf-8') as templatefile:
            print(template.Template(templatefile.read()).render(**display))
except AttributeError:
    pass
