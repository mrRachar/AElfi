import yaml, os

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
        if document.get('Paths'):
            htaccess.rewrites = [
                    (name, redirect['when'], redirect['from'], redirect['to'], redirect.get('options', ''))
                    for name, redirect in document['Paths'].items()
                ]
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
            representation += 'ErrorDocument {number} "{file}"\n'.format(number=error, file=self.reltoabs_path(document))
        for name, rules, collect, destination, options in self.rewrites:
            representation += '\n#{}\n'.format(name)
            for rule in (rules if isinstance(rules, list) else (rules,)):
                representation += 'RewriteCond %{{REQUEST_FILENAME}} {when}\n'.format(when=rule)
            representation += 'RewriteRule "{collect}" "{destination}"{options}\n'.format(rule=rule, collect=collect,
                                                                                          destination=self.reltoabs_path(destination),
                                                                                          options = ' [' + options + ']'
                if options else '')
        return representation

    @staticmethod
    def reltoabs_path(path: str, location: str='../') -> str:
        if path == '':
            return ''
        if path.startswith('text:'):
            return path[5:]
        actual_dir = os.getcwd()
        os.chdir(location)
        absolute_path = os.path.abspath(path)
        os.chdir(actual_dir)
        return absolute_path

if __name__ == '__main__':
    with open('../.htaccess', 'w') as htaccess_file:
        htaccess = HTAccessDocument.fromyaml(open('../aelfi.conf'), page=1)
        htaccess.rewrites.insert(0, ('Python Documents Redirect', ['.py'], "^(.*)$", "AElfi/loader.py?AELFI_PAGE=$1", "L,QSA"))
        htaccess.rewrites.insert(1, ('Aelfi Config File Protection', ['^/aelfi.config$'], "^.*$", "", "F"))
        htaccess.rewrites.insert(1, ('Template File Protection', ['.template$'], "^.*$", "", "F"))
        htaccess.require = 'all granted'
        htaccess.options = '+ExecCGI -Indexes'
        htaccess.handlers = ['cgi-script .py .pl']
        htaccess.indices = ["index.py", "index.php", "index.html", "index.htm",
                            "index.xml", "index.txt", "index.jpg", "index.png",
                            "index.gif", "index.jpeg", "index.pl"]
        htaccess_file.write(str(htaccess))