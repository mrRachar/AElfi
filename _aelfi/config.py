import json
from importlib.machinery import SourceFileLoader

class Configuration:
    """The configurations that the user has chosen for AElfi in general"""

    charset = 'utf-8'

    def __init__(self, file_location: str, *, page=0):
        """Create a new structure to store confifurations, from a YAML file

        :param file_location: str - Where the yaml file is located
        :param page: int - If there are multiple documents in the file, which one to load
        """

        # Open the file to read
        with open(file_location) as file:
            config = json.load(file)

        # Store what charset to send documents as being by default
        self.charset = config['charset']

        # Store the templating module specified
        if 'template' not in config:
            config['template'] = 'mako'

        # Load template module from file
        self.template_module = SourceFileLoader('template_' + config['template'], './templating/{}.py'.format(config['template'])).load_module()
        self.template_module_name = config['template']
