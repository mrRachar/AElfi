import builtins, os

request = builtins.request
response = builtins.response
try:
    os.chdir(builtins.request.directory)
except AttributeError:
    pass
print = response.print
exec(builtins.request.page)
