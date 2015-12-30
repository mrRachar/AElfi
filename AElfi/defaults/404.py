from mako.template import Template

response.header['Status'] = '404'
display['title'] = 'You\'re Lost [404]'
display['header'] = 'You\'re Lost'
display['message'] = '''Hmm. Are you sure you got the right place? It's just that where you want to go, doesn't exist!<br/>You tried to go to:'''
display['destination'] = request.args['sourcepage']

print(Template('''<html>
    <head>
        <title>${title}</title>
    </head>
    <body>
        <h2>${header}</h2>
        <p>${message}</p>
        <small>${destination | h}</p>
    </body>
</html>''').render(**display))