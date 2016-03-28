import yaml
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
            # Get the requested page of the YAML file
            config = tuple(yaml.safe_load_all(file))[page]

        # Store what charset to send documents as being by default
        self.charset = config['Charset']

        # Store the templating module specified
        if 'Template-Module' not in config:
            config['Template-Module'] = 'mako'

        self.template_module = SourceFileLoader(config['Template-Module'], './templating/{}.py'.format(config['Template-Module'])).load_module()
        #module_specs = importlib.util.spec_from_file_location(, )
        #self.template_module = importlib.util.module_from_spec(module_specs)
        #module_specs.loader.exec_module(self.template_module)
        self.template_module_name = config['Template-Module']
