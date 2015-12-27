import yaml, re

class Configuration:
    def __init__(self, file_location: str):
        with open(file_location) as file:
            config = yaml.load(file)
        self.indecies = config['Index']
        self.errorresponses = {}
        for error, action in config['Error'].items():
            if action.startswith('text:'):
                self.errorresponses[int(error)] = 'txt', action[5:]
            else:
                with open('../' + action) as response:
                    self.errorresponses[int(error)] = action.split('.')[-1], response.read()
        self.extensions = {}
        for name, extension in config['Extensions'].items():
            for ext in extension['extensions']:
                self.extensions[ext] = extension['content-type']

        self.protected = config['Protected']
        self.charset = config['Charset']
    def isprotected(self, file):
        for regex in self.protected:
            if re.match(regex, file[3:]):
                return True
        else:
            return False
