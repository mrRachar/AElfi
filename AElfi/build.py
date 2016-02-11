#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

import yaml, os, re

class HTAccessDocument:
    error_documents = {}
    rewrites = []
    require = ''
    options = ''
    handlers = []
    indices = []
    rewrite_engine = True

    @classmethod
    def fromyaml(cls, file, *, page: int=0):
        document = tuple(yaml.safe_load_all(file))[page]
        try:
            file.close()
        except AttributeError:
            pass

        htaccess = cls()
        if document.get('Errors'):
            htaccess.error_documents = document['Errors']
        if document.get('Protect'):
            htaccess.rewrites = [
                ('Protect "{}"'.format(directory), ['^'+re.escape(cls.cleanpath('./', toabsolute=True)+'/'+directory) + '.*\.py$'], '(.*)', '$1',
                 'END,H=text/plain')
                for directory in document['Protect']
                ]
        if document.get('Paths'):
            htaccess.rewrites += [
                    (name, redirect['when'], redirect['from'], redirect['to'], redirect.get('options', ''))
                    for name, redirect in document['Paths'].items()
                ]
        if document.get('Index'):
            htaccess.indices = list(document['Index'])
        return htaccess

    def __str__(self):
        representation = ''

        if self.require:
            representation += 'Require {}\n'.format(self.require)

        if self.options:
            representation += 'Options {}\n'.format(self.options)

        for handler in self.handlers:
            representation += 'AddHandler {}\n'.format(handler)

        if self.indices:
            representation += 'DirectoryIndex {}\n'.format(' '.join(self.indices))

        representation += 'RewriteEngine {}\n'.format('on' if self.rewrite_engine else 'off')

        for error, document in sorted(self.error_documents.items()):
            representation += 'ErrorDocument {number} "{file}"\n'.format(number=error, file=self.cleanpath(document, toabsolute=True))
        for name, rules, collect, destination, options in self.rewrites:
            representation += '\n#{}\n'.format(name)
            for rule in (rules if isinstance(rules, list) else (rules,)):
                representation += 'RewriteCond %{{REQUEST_FILENAME}} {when}\n'.format(when=rule)
            representation += 'RewriteRule "{collect}" "{destination}"{options}\n'.format(rule=rule, collect=collect,
                                                                                          destination=self.cleanpath(destination),
                                                                                          options = ' [' + options + ']'
                if options else '')
        return representation

    @staticmethod
    def cleanpath(path: str, location: str='./', toabsolute: bool=False) -> str:
        if path.startswith('text:'):
            return path[5:]
        elif not toabsolute or path == '':
            return path

        actual_dir = os.getcwd()
        os.chdir(location)
        absolute_path = os.path.abspath(path)
        os.chdir(actual_dir)
        return absolute_path

if __name__ == '__main__':
    if os.getcwd().endswith('AElfi'):
        print('Please make sure to run this tool from the projects root directory, not the `AELfi` folder!\nRunning Anyway...\n')
    
    with open('./.htaccess', 'w') as htaccess_file:
        htaccess = HTAccessDocument.fromyaml(open('./aelfi.conf'), page=1)
        htaccess.rewrites.append(('Python Documents Redirect', ['.py$'], "^(.*)$", "AElfi/loader.py?AELFI_PAGE=$1", "L,QSA"))
        htaccess.rewrites.insert(0,
                    ('Aelfi Config File Protection', ['^'+re.escape(htaccess.cleanpath('./', toabsolute=True)) + '/aelfi\.conf$'], "^.*$", "", "F"))
        htaccess.rewrites.insert(0, ('Template File Protection', ['\.template$'], "^.*$", "", "F"))
        htaccess.require = 'all granted'
        htaccess.options = '+ExecCGI -Indexes'
        htaccess.handlers = ['cgi-script .py .pl']
        if not htaccess.indices:
            htaccess.indices = ["index.py", "index.php", "index.html", "index.htm",
                                "index.xml", "index.txt", "index.jpg", "index.png",
                                "index.gif", "index.jpeg", "index.pl"]
        htaccess_file.write(str(htaccess))
        print('built!')
