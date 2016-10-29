## Magic Templates

One of the great things about AElfi is how easily it lets you build your web apps, without them getting them too messy. Magic Templates are at the 
core of the way AElfi splits up the view from the model and controller.

Saving any file to the same name, except with the template extension, so `index.py` and `index.view`, will mean when the Python script is finished, 
the template file will automagically be run. This means you don't have to call it or anything, and you can just put all you *view* code in the 
template file.

In the global scope of any AElfi-run Python script is the `display` variable. This is a dictionary in which you can put the variables you want sent to 
the display. Just fill them in here, and the display will have access to them. The `display` variable already has the request and response 
variables in it, so you don't need to add them yourself.

The templating system uses [**mako** templates](http://www.makotemplates.org/), which are very fast and very quick, and have many features to make 
making templates very easy. However, it is very easy to change which templating engine is used. To do this, just create a copy of mako.py, calling it
something like jinja2.py, and edit it to fit that templating engine's interface. Then in the build file, add a template use-declaration: `use 
template jinja2`.

A quick example showing the user their IP address using templates:

*ipaddressexample.py*
```python
#Add the user_ip for the template
display['user_ip'] = request['ip']
```
*ipaddressexample.view*
```mako
<html>
	<head>
		<title>Your IP Address</title>
	</head>
	<body>
		<p>Your IP address is: ${user_ip}</p>
	</body>
</html>
```

***Note:*** *Headers will automatically be sent after the Python code has executed, before the template is run*

***Also Note:*** *`request` and `response` are automatically already in the `display` dictionary for you*

***Finally Note:*** *If using your own templates, you can be assured that AElfi tools update system __will__ transfer them across, but will not 
protect any changes you make to the `mako.py` file* 