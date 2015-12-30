import yaml, re

class Configuration:
    def __init__(self, file_location: str):
        with open(file_location) as file:
            config = yaml.load(file)
        self.errorresponses = {}
        for error, action in config['Error'].items():
            if action.startswith('text:'):
                self.errorresponses[int(error)] = 'txt', action[5:].encode('utf-8')
            else:
                with open('../' + action) as response:
                    self.errorresponses[int(error)] = action.split('.')[-1], response.read()
        self.charset = config['Charset']
