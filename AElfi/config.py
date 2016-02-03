import yaml

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
