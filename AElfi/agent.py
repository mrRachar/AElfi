import re

class Agent:
    """A representation of the user's browser, agent, device, etc."""
    os = {
        'name': 'OS',
        'version': '0'
    }
    istouch = False
    type = 'desktop'
    system = '32'
    device = 'computer'
    browser = {
        'name': 'browser',
        'version': '0',
        'engine': {
            'name': 'engine',
            'version': '0'
        }
    }

    def __init__(self, useragent: str=None, **kwargs):
        """Create a new user agent, either giving a string to pass, or keywords for values, or both

        :param useragent:Optional[str] - the user agent string, to digest
        :param kwargs -
            os: dict - The agent's operating system, a dict of 'name', and 'version'
            touch: str - is the device a touch screen
            type: str - Is the agent a desktop, mobile or tablet
            device: str - Brand or manufacturer of device: Mac, HTC, LG or any other
            browser: dict - The agent's browser system, a dict of 'name', and 'version', and a sub-dict under 'engine' containing the same
        """

        # If a user agent string has been given
        if useragent:
            breakdown = self.digest(useragent) #Break it down into a dictionary
            #Assign the breakdown to the fields
            self.os = breakdown['os']
            self.istouch = breakdown['touch']
            self.type = breakdown['type']
            self.system = breakdown['system']
            self.device = breakdown['device']
            self.browser = breakdown['browser']

        #If any of these have been given as kwargs, use them instead of current value, or digested value
        self.os = kwargs.get('os', self.os)
        self.istouch = kwargs.get('touch', self.istouch)
        self.type = kwargs.get('type', self.type)
        self.system = kwargs.get('system', self.system)
        self.device = kwargs.get('device', self.device)
        self.browser = kwargs.get('browser', self.browser)

    def __repr__(self) -> str:
        """Display a representation of the object, which can be used to instantiate a similar object

        :return the description of the object, giving complete state, in constructor form
        """

        return '{}(os={!r}, system={!r}, type={!r}, device={!r}, touch={!r}, browser={!r})'.format(
            self.__class__.__name__,
            self.os,
            self.system,
            self.type,
            self.device,
            self.istouch,
            self.browser
        )

    @classmethod
    def digest(self, string):
        """Works out the meaning of a given string, returning the digest as a parsed dictionary"""

        # Set some default values for the digest
        digest = {
            'device': '',
            'os': {'name': '', 'version': ''},
            'touch': False,
            'system': '32/64',
            'type': 'desktop'
        }
        # See if it could be a user agent
        if not re.match(r'[A-Za-z]+/\d*.\d*\s*\(.*?\)(?:\s*.*)?', string):
            return None # If it couldn't, return no digest

        digest['base'] = {}
        digest['base']['name'], digest['base']['version'], core, branch = \
            re.match(r'([A-Za-z]+)/(\d*.\d*)\s*\((.*?)\)(?:\s*(.*))?', string).groups()

        ## Main device checking ##
        
        if self.any_in(core, 'iPad', 'iPhone', 'Macintosh'):
            if 'iPad' in core:
                digest['device'] = 'iPad'
                digest['os']['name'] = 'iOS'
                digest['type'] = 'tablet'
                digest['touch'] = True
            elif 'iPhone' in core:
                digest['device'] = 'iPhone'
                digest['os']['name'] = 'iOS'
                digest['type'] = 'mobile'
                digest['touch'] = True
            elif 'Mac OS X' in core:
                digest['device'] = 'Mac'
                digest['os']['name'] = 'Mac OS X'
            elif 'Macintosh' in core:
                digest['device'] = 'Mac'
                digest['os']['name'] = 'Mac OS'
                digest['touch'] = False
            if re.search(r'\d+_\d+(?:_\d+)?', core):
                digest['os']['version'] = re.search(r'(\d+_\d+(?:_\d+)?)', core) \
                                            .group(1).replace('_', '.')
        elif 'Android' in core:
            digest['os']['name'] = 'Android'
            digest['type'] = 'mobile' if ' mobile ' in branch.lower() else 'tablet'
            digest['device'] = 'LG' if 'LG' in core.upper() else            \
                               'HTC' if 'HTC' in core.upper() else          \
                               'Motorola' if 'Moto' in core.lower() else    \
                               'Motorola' if 'XT' in core.upper() else      \
                               'Nexus' if 'nexus' in core.lower() else      \
                               'Samsung' if 'samsung' in core.upper() else  \
                               'Smartphone'
            digest['os']['version'] = re.search(r'(\d+\.\d+(?:\.\d+)?)', core).group(1)
            digest['touch'] = True

        elif 'Windows Phone' in core:
            digest['os']['name'] = 'Windows Phone'
            digest['os']['version'] = re.search(r'Windows Phone (\d+.\d+)', core).group(1)
            digest['device'] = 'HTC' if 'HTC' in core else      \
                               'Lumia' if 'Lumia' in core else  \
                               'Smartphone'
            digest['touch'] = True
            digest['type'] = 'mobile'

        elif 'Windows' in core:
            digest['os']['name'] = 'Windows'
            digest['os']['version'] = \
                                    '2000' if 'NT 5.0' in core else     \
                                    'XP' if 'NT 5.1' in core else       \
                                    'Vista' if 'NT 6.0' in core else    \
                                    '7' if 'NT 6.1' in core else        \
                                    '8' if 'NT 6.2' in core else        \
                                    '8.1' if 'NT 6.3' in core else      \
                                    '10' if 'NT 10' in core else        \
                                    'NT' if 'NT' in core else ''
            digest['touch'] = False if 'touch' not in core else True
            digest['system'] = '64' if self.any_in(core, 'WOW64', 'Win64') \
                else '32'

        
        elif 'Linux' in core:
            digest['os']['name'] = 'Linux'

        ## Browser check ##
        browser = digest['browser'] = {
            'name': '',
            'version': '',
            'engine': {
                'name': '',
                'version': ''
            }
        }
        if digest['base']['name'] == 'Opera':
            browser['name'] = 'Opera'
            browser['version'] = re.search(r'Version/([0-9\.]+)', branch).group(1)
            browser['engine']['name'] = 'Presto'
            browser['engine']['version'] = re.search(r'Presto/([0-9\.]+)', branch).group(1)

        elif 'OPR' in branch:
            browser['name'] = 'Opera'
            browser['version'] = re.search(r'OPR/([0-9\.]+)', branch).group(1)
            browser['engine']['name'] = 'Blink' if int(browser['version'].split('.')[0]) >= 15 else 'Webkit'
            browser['engine']['version'] = re.search(r'AppleWebKit/([0-9\.]+)', branch).group(1)

        elif 'Edge' in branch:
            browser['name'] = 'Edge'
            browser['version'] = re.search(r'Edge/([0-9\.]+)', branch).group(1)
            browser['engine']['name'] = 'EdgeHTML'
            browser['engine']['version'] = re.search(r'AppleWebKit/([0-9\.]+)', branch).group(1)

        elif 'Chrome' in branch:
            browser['name'] = 'Chrome'
            browser['version'] = re.search(r'Chrome/([0-9\.]+)', branch).group(1)
            browser['engine']['name'] = 'Blink' if int(browser['version'].split('.')[0]) >= 28 else 'Webkit'
            browser['engine']['version'] = re.search(r'AppleWebKit/([0-9\.]+)', branch).group(1)

        elif 'Safari' in branch:
            browser['name'] = 'Safari'
            browser['version'] = re.search(r'Version/([0-9\.]+)', branch).group(1)
            browser['engine']['name'] = 'Webkit'
            browser['engine']['version'] = re.search(r'AppleWebKit/([0-9\.]+)', branch).group(1)

        elif 'Firefox' in branch:
            browser['name'] = 'Firefox'
            browser['version'] = re.search(r'Firefox/([0-9\.]+)', branch).group(1) or ''
            browser['engine']['name'] = 'Gecko'
            browser['engine']['version'] = re.search(r'Gecko/([0-9\.]+)', branch).group(1)


        elif 'MSIE' in core:
            browser['name'] = 'MicroSoft Internet Explorer (MSIE)'
            browser['version'] = re.search(r'MSIE ([0-9]+.[0-9]+)', core).group(1)
            browser['engine']['name'] = 'Trident'
            if re.search(r'Trident/([0-9\.]+)', core):
                browser['engine']['version'] = re.search(r'Trident/([0-9\.]+)', core).group(1)

        return digest

    @staticmethod
    def any_in(iterable, *list_):
        return any(word in iterable for word in list_)
