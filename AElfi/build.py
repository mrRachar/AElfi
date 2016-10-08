#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

import yaml, os, re

class Rewrite:
    name = ''
    conditions = []
    collect = ''
    destination = ''
    options = []

    def __init__(self, name: str=None, conditions: list=None, collect: str=None, destination: str=None, options: list=None):
        self.name = str(name if not name is None else self.name)
        self.conditions = conditions if not conditions is None else list(self.conditions)
        self.collect = str(collect if not collect is None else self.collect)
        self.destination = str(destination if not destination is None else self.destination)
        self.options = options if not options is None else list(self.options)

    def __str__(self) -> str:
        string = '#{}\n'.format(self.name)
        for value, condition in self.conditions:
            string += 'RewriteCond {value} {condition}\n'.format(value=value, condition=condition)
        string += 'RewriteRule "{self.collect}" "{self.destination}"'.format(self=self)
        if self.options:
            string += ' [{options}]'.format(options=','.join(self.options))
        string += '\n'
        return string

    @classmethod
    def of_protect(cls, directory: str):
        return cls(
                    name='Protect "{}"'.format(directory),
                    conditions=[('%{REQUEST_FILENAME}', '^'+re.escape(HTAccessDocument.cleanpath(directory, toabsolute=True)) + '.*\.py$')],
                    collect='(.*)',
                    destination='$1',
                    options=['END', 'H=text/plain']
                )

    @classmethod
    def of_hide(cls, path):
        return cls(
                    name='Hide "{}"'.format(path),
                    conditions=[('%{REQUEST_FILENAME}', '^'+re.escape(HTAccessDocument.cleanpath(path, toabsolute=True)))],
                    collect='(.*)',
                    destination='-',
                    options=['R=404']
                )

    @classmethod
    def of_forbid(cls, path):
        return cls(
                    name='Forbid "{}"'.format(path),
                    conditions=[('%{REQUEST_FILENAME}', '^'+re.escape(HTAccessDocument.cleanpath(path, toabsolute=True)))],
                    collect='(.*)',
                    destination='-',
                    options=['F']
                )

class HTAccessDocument:
    error_documents = {}
    rewrites = []
    require = ''
    options = ''
    handlers = []
    indices = []
    rewrite_engine = True

    def __init__(self):
        self.error_documents = {}
        self.rewrites = []
        self.handlers = []
        self.indices = []

    @classmethod
    def fromyaml(cls, file, *, page: int=0):
        document = tuple(yaml.safe_load_all(file))[page]
        try:
            file.close()
        except AttributeError:
            pass

        htaccess = cls()

        # In the case that there are no directives
        if document is None:
            return htaccess

        if document.get('Errors'):
            htaccess.error_documents = document['Errors']

        if document.get('Hide'):
            htaccess.rewrites = [
                Rewrite.of_hide(path) for path in document['Hide']
                ]

        if document.get('Forbid'):
            htaccess.rewrites += [
                Rewrite.of_forbid(path) for path in document['Forbid']
                ]

        if document.get('Protect'):
            htaccess.rewrites += [
                Rewrite.of_protect(directory) for directory in document['Protect']
                ]
        if document.get('Paths'):
            rewr_var = lambda v: "%{" + v.upper().replace(' ', '_').replace('-', '_') + "}"
            htaccess.rewrites += [
                    Rewrite(
                        # Title
                        name,
                        # When
                        ([(rewr_var(redirect.get('var', 'request-uri')), when)
                                    for when in redirect['when']]
                                if isinstance(redirect['when'], list)
                                else [(rewr_var(redirect.get('var','request-uri')), redirect['when'])])
                            if 'when' in redirect else [],
                        # From
                        redirect['from'],
                        # To
                        redirect['to'],
                        # Options
                        list(
                            set(redirect.get('options', []))
                            if isinstance(redirect.get('options', []), list)
                            else {redirect.get('options')}
                        ) if redirect.get('options', '') != 'default' else ['QSA']
                    ) for name, redirect in document['Paths'].items()
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
            representation += 'ErrorDocument {number} "{file}"\n'.format(number=error, file=self.cleanpath(document, toabsolute=False))

        for rewrite in self.rewrites:
            representation += '\n{!s}'.format(rewrite)
        return representation

    @staticmethod
    def cleanpath(path: str, location: str='./', toabsolute: bool=False) -> str:
        if path.startswith('text:'):
            return path[5:]
        elif not toabsolute or path == '':
            return path

        if location != './':
            actual_dir = os.getcwd()
            os.chdir(location)
        absolute_path = os.path.abspath(path)
        if location != './':
            os.chdir(actual_dir)
        return absolute_path


if __name__ == '__main__':
    if os.getcwd().endswith('AElfi'):
        print('Please make sure to run this tool from the projects root directory, not the `AELfi` folder!\nRunning Anyway...\n')

    with open('./.htaccess', 'w') as htaccess_file:
        htaccess = HTAccessDocument.fromyaml(open('./aelfi.conf'), page=1)
        htaccess.rewrites.append(Rewrite('Python Documents Redirect', [('%{REQUEST_FILENAME}', '.py$'), ('%{REQUEST_FILENAME}', '-f')], "^(.*)$", "AElfi/loader.py?AELFI_PAGE=$1", ["END", "L", "QSA"]))
        htaccess.rewrites.insert(0,
                    Rewrite('Index counter-protection', [('%{REQUEST_FILENAME}', '^'+re.escape(htaccess.cleanpath('./', toabsolute=True)) + '/?$')], "^(.*)$", "$1", ["END", "L", "QSA"]))
        htaccess.rewrites.insert(0,
                    Rewrite('AElfi folder protection', [('%{REQUEST_FILENAME}', '^'+re.escape(htaccess.cleanpath('./', toabsolute=True)) + '/AElfi/')], "^.*$", "", ["F"]))
        htaccess.rewrites.insert(0,
                    Rewrite('Aelfi Config File Protection', [('%{REQUEST_FILENAME}', '^'+re.escape(htaccess.cleanpath('./', toabsolute=True)) + '/aelfi\.conf$')], "^.*$", "", ["F"]))
        htaccess.rewrites.insert(0, Rewrite('View File Protection', [('%{REQUEST_FILENAME}', '\.view$')], "^.*$", "", "F"))
        htaccess.require = 'all granted'
        htaccess.options = '+ExecCGI -Indexes'
        htaccess.handlers = ['cgi-script .py .pl']
        if not htaccess.indices:
            htaccess.indices = ["index.py", "index.php", "index.html", "index.htm",
                                "index.xml", "index.txt", "index.jpg", "index.png",
                                "index.gif", "index.jpeg", "index.pl"]
        try:
            mod_folder, module_dirs = next(os.walk('AElfi/modules'))[:2]
            for module_dir in module_dirs:
                try:
                    module_htaccess = HTAccessDocument.fromyaml(open(mod_folder + '/' + module_dir + '/aelfi.conf'))
                    htaccess.indices += module_htaccess.indices
                    htaccess.rewrites += module_htaccess.rewrites
                except:
                    continue
        except:
            pass
        htaccess_file.write(str(htaccess))
        print('built!')
