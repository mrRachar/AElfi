from collections import namedtuple
from enum import Enum
from itertools import zip_longest
from abc import ABC, abstractmethod
import re, os, json

from antlr4 import *

from .BuildLexer import BuildLexer
from .BuildParser import BuildParser
from .functions import string_swap, escape_capturegroups

class Originatable(ABC):
    value = ''
    registry = {}

    @abstractmethod
    def build_asorigin(self) -> str: pass


class Matcherable(ABC):
    @abstractmethod
    def build_asmatcher(self) -> str: pass


class Flaggable(ABC): pass


class ExpressionObject(ABC):
    value = ''

    @abstractmethod
    def build(self, *, registry=None) -> str: pass

    def __repr__(self) -> str:
        return '{}(value={!r})'.format(self.__class__.__name__, self.value)


class Variable(ExpressionObject):
    variables = {
            'ip':                   'REMOTE_ADDR',
            'language':             'HTTP_ACCEPT_LANGUAGE',
            'server.ip':            'SERVER_ADDR',
            'server.name':          'SERVER_NAME',
            'server.port':          'SERVER_PORT',
            'time.stamp':           'TIME',
            'time.day':             'TIME_DAY',
            'time.dayofweek':       'TIME_WDAY',
            'time.hour':            'TIME_HOUR',
            'time.minute':          'TIME_MINUTE',
            'time.month':           'TIME_MON',
            'time.second':          'TIME_SEC',
            'time.year':            'TIME_YEAR',
            'method':               'REQUEST_METHOD',
            'connection':           'CONNECTION',
            'location':             'REQUEST_URI',
            'protocol':             'REQUEST_PROTOCOL',
            'filepath':             'REQUEST_FILENAME',
        }
    regex = re.compile(r"(?:^|[^{]){(\w+)\}")

    def __init__(self, value: str):
        if value.startswith(':'):
            value = value[1:-1]
        self.value = value

    def build(self, *, registry=None) -> str:
        try:
            return '%{{{}}}'.format(self.variables[self.value])
        except KeyError:
            try:
                if self.value.isnumeric():
                    return '${}'.format(self.value)
                else:
                    return '${}'.format((registry or {})[self.value])
            except KeyError as e:
                raise KeyError from e



class Capture(Variable):
    regex = re.compile(r"(?:^|[^{]){([\w ]+)(?:\:((?:\\\}|[^}])+))?\}")

    def __init__(self, value: str, pattern: str):
        super().__init__(value)
        self.pattern = pattern

    def __repr__(self) -> str:
        return '{}(value={!r}, pattern={!r})'.format(self.__class__.__name__, self.value, self.pattern)

    def build(self, *, registry=None) -> str:
        return '({})'.format(self.pattern)


class Method(Variable, Matcherable):
    def build(self, *, registry=None) -> str:
        return ' {}'.format({
            '.isfile':              '-f',
            '.isdirectory':         '-d',
            '.hastext':             '-s',
        }.get(self.value, self.value.upper()))

    def build_asmatcher(self) -> str:
        return self.build()


class String(ExpressionObject, Matcherable):
    def __init__(self, value: str):
        if value.startswith(('"', "'")):
            value = value[1:-1]
        self.value = value.replace(r"\'", "'").replace(r'\"', '"').replace(r"\\", "\\")

    def _build(self, *, registry=None) -> str:
        build_string = self.value
        interpolation = Variable.regex.search(build_string)
        while interpolation:
            variable = Variable(interpolation.group(1))
            build_string = build_string[:interpolation.span(1)[0]-1] + variable.build(registry=registry) + build_string[interpolation.span(1)[1]+1:]
            interpolation = Variable.regex.search(build_string)
        return build_string

    def build(self, *, registry=None):
        return '"{!s}"'.format(self._build(registry=registry).replace('"', '\\"'))

    def build_asmatcher(self) -> str:
        return '"{!s}"'.format(re.escape(self.value.replace('"', '\\"')))


class Regex(String, Originatable):
    def __init__(self, value: str):
        if value.startswith('`'):
            value = value[1:-1]
        super().__init__(value.replace(r"\>", ">").replace(r'\<', '<').replace("\\\\", "\\"))

    build_asorigin = build_asmatcher = lambda self, *args, **kwargs: self.build(*args, **kwargs)


class Path(String, Originatable, Flaggable):
    flags = ''
    flag_sets = frozenset({
        # Relative, Absolute, Incomplete/Ignore, errordoc syntax (¦) (default normally i, except origin/destination then r)
        frozenset({'r', 'a', 'i', '¦'}),
        # Unescape, Escape (default normally unescape except magic dots)
        frozenset({'u', 'e'})
    })

    def __init__(self, value: str, flags=''):
        prefix_match = re.match('(?:([aArRiI])([dDeE])?|([dDeE])([aArRiI])?)?\<', value)
        if value.startswith('<'):
            value = value[1:-1]
        elif prefix_match:
            value = value[len(prefix_match.group()):-1]
            for group in prefix_match.groups():
                if isinstance(group, str):
                    self.flags += group.lower()
        self.flags += flags
        super().__init__(value)

    def __repr__(self) -> str:
        return '{}(value={!r}, flags={!r})'.format(self.__class__.__name__, self.value, self.flags)

    def build(self, *, registry=None, flags=None):
        return '"{!s}"'.format(self.apply_flags(string=self._build(registry=registry).replace('"', '\\"'), flags=flags))

    def build_asmatcher(self, flags=None):
        return '"{!s}"'.format(self.apply_flags(string=self._build(registry=None), flags=flags))

    def apply_flags(self, flags=None, *, string=None):
        flags = self.get_flags(flags)
        applied = self.value if string is None else string

        if 'r' in flags or '¦' in flags:
            applied = os.path.relpath(applied)
            if '¦' in flags:
                applied = '/' + applied
        elif 'a' in flags:
            applied = '^' + os.path.abspath(applied)

        if 'e' in flags:
            applied = escape_capturegroups(re.escape(applied))
        elif 'u' not in flags:
            applied = string_swap(applied, '\\.', '.')
            applied = escape_capturegroups(applied)
        return applied

    def get_flags(self, extra=None) -> str:
        flags = ''
        for flag in self.flags + (extra or ''):
            for flag_set in self.flag_sets:
                if flag in flag_set:
                    break
            if not any(x in flags for x in flag_set):
                flags += flag
        return flags


    def build_asorigin(self, flags=None) -> str:
        build_string = self.apply_flags(flags='r', string=self.value)
        self.registry = {}

        group_number = 1
        interpolation = Capture.regex.search(build_string)
        while interpolation:
            capture = Capture(interpolation.group(1), pattern=interpolation.group(2) or '[A-Za-z0-9][A-Za-z0-9-]*')
            build_string = build_string[:interpolation.span(1)[0]-1] + capture.build() + build_string[interpolation.span()[1]:]
            self.registry[capture.value] = group_number

            interpolation = Capture.regex.search(build_string)
            group_number += 1

        build_string = build_string.replace('"', '\\"')
        return '"{!s}"'.format(build_string)


class Condition(namedtuple('Condition', ['operator', 'left', 'right', 'negate'])):
    class Operator(Enum):
        and_ = '&'
        or_ = '|'
        none = None

    def build(self, *, registry=None) -> str:
        left = self.left.build(registry=registry)
        right = self.right.build_asmatcher()
        return 'RewriteCond {l} {n}{r}'.format(
                                                n='!' if self.negate else '',
                                                l=left,
                                                r=right
                                            )

    @property
    def operator_string(self) -> str:
        return {self.Operator.or_: '[OR]'}.get(self.operator, '')

    @classmethod
    def from_node(cls, node, *, operator: (str, Operator)=Operator.none):
        if operator in ('&', '|'):
            operator = cls.Operator.and_ if operator == '&' else cls.Operator.or_
        elif not isinstance(operator, cls.Operator):
            operator = cls.Operator.none

        negate = False
        if node.children[0].getText() == '!':
            negate = True
            node.children.pop(0)

        leftnode = node.children[0]
        rightnode = node.children[1]
        left = Path(leftnode.getText())                         \
                if leftnode.getText().startswith('<')           \
                else String(leftnode.getText())                 \
                if leftnode.getText().startswith(('"', "'"))    \
                else Variable(leftnode.getText())
        right = Path(rightnode.getText())                       \
                if rightnode.getText().startswith('<')          \
                else String(rightnode.getText())                \
                if rightnode.getText().startswith(('"', "'"))   \
                else Method(rightnode.getText())                \
                if rightnode.getText().startswith('.')          \
                else Regex(rightnode.getText())
        return cls(operator, left, right, negate)


class SpecialDestination(String):
    destinations = {'forbid', 'none', 'protect', 'error'}
    def __init__(self, value: str):
        self.options = {
            'forbid': ['END', 'F'],
            'none': ['R=404'],
            'protect': ['END', 'H=text/plain'],
            'error': ['R=500']
        }.get(value, set())
        super().__init__(value)


class Route(namedtuple('Route', ['destination', 'origins', 'conditions', 'options'])):
    @classmethod
    def from_statement(cls, statement):
        if statement.children[0].getText() in SpecialDestination.destinations:
            destination = SpecialDestination(statement.children[0].getText())
        else:
            destination = Path(statement.children[0].getText())
        origins = []
        conditions = []
        for child, precursor in zip(statement.children[2::2], statement.children[1::2]):
            if isinstance(child, BuildParser.ConditionContext):
                conditions.append(Condition.from_node(child, operator=precursor.getText()))
            elif child.getText().startswith("`"):
                origins.append(Regex(child.getText()))
            else:
                origins.append(Path(child.getText()))
        return cls(destination, origins, conditions, ['L', 'QSA'])

    def build(self) -> str:
        build_string = "# " + self.destination.value
        options = self.options.copy()

        for origin in self.origins:
            build_string += '\n'

            binary_operators = (' ' + condition.operator_string + ' ' for condition in self.conditions[1:])
            for condition, binary_operator in zip_longest(self.conditions, binary_operators, fillvalue=''):
                build_string += condition.build(registry=origin.registry) + binary_operator + '\n'

            built_origin = origin.build_asorigin()              \
                            if not isinstance(origin, Flaggable) \
                            else origin.build_asorigin(flags='r')

            if isinstance(self.destination, SpecialDestination):
                built_dest = '-'
                options += self.destination.options
            elif isinstance(self.destination, Flaggable):
                built_dest = self.destination.build(registry=origin.registry, flags='r')
            else:
                built_dest = self.destination.build(registry=origin.registry)

            build_string += "RewriteRule {} {} [{}]\n".format(built_origin, built_dest, ','.join(options))
        return build_string


class ErrorReroute(namedtuple('ErrorReroute', ['destination', 'error'])):
    error_names = {
        'forbid':   403,
        'error':    500,
        'none':     404
    }

    @classmethod
    def from_statement(cls, statement):
        if statement.children[0].getText().startswith("<"):
            destination = Path(statement.children[0].getText())
        else:
            destination = String(statement.children[0].getText())
        try:
            error = int(statement.children[2].getText())
        except ValueError:
            error = cls.error_names[statement.children[2].getText()]
        return cls(destination, error)

    def build(self) -> str:
        if isinstance(self.destination, Flaggable):
            built_dest = self.destination.build(flags='¦u')
        else:
            built_dest = self.destination.build()
        return "ErrorDcoument {} {}\n".format(self.error, built_dest)


class Build:
    lang = 'python3'
    template = 'mako'
    charset = 'utf8'
    routes = []
    libraries = []
    options = ''
    handlers = []
    require = 'all granted'
    indices = []
    rewrite_engine = True

    def __init__(self, **values):
        if not values:
            return
        self.lang = values.get('lang', self.lang)
        self.template = values.get('template', self.template)
        self.charset = values.get('charset', self.charset)
        self.routes = values.get('routes', list(self.routes))
        self.libraries = values.get('routes', list(self.libraries))

    @classmethod
    def from_file(cls, file_location: str):
        with open(file_location) as file:
            if not file.read().strip('\n \r'):
                return cls()
        filestream = FileStream(file_location)
        lexer = BuildLexer(filestream)
        stream = CommonTokenStream(lexer)
        parser = BuildParser(stream)
        return cls.from_tree(parser.programme())

    @classmethod
    def from_tree(cls, tree: BuildParser.ProgrammeContext):
        build = cls()
        for line in tree.children:
            statement = line.children[0]
            if isinstance(statement, BuildParser.DeclarationContext):
                declaration = statement.children[0]
                if isinstance(declaration, BuildParser.Use_declarationContext):
                    declaration_aspect = declaration.children[1].getText()
                    declaration_value = declaration.children[2].getText()
                    setattr(build, declaration_aspect, declaration_value)
                elif isinstance(declaration, BuildParser.Include_declarationContext):
                    build.libraries.append(Path(declaration.children[1].getText()))
            elif isinstance(statement, BuildParser.RouteContext):
                if BuildParser.symbolicNames[statement.children[2].symbol.type] in ('ERROR_CODE', 'ERROR_NAME'):
                    build.routes.append(ErrorReroute.from_statement(statement))
                else:
                    build.routes.append(Route.from_statement(statement))
        return build

    def build_htaccess(self) -> str:
        build_string = ''

        if self.require:
            build_string += 'Require {}\n'.format(self.require)

        if self.options:
            build_string += 'Options {}\n'.format(self.options)

        for handler in self.handlers:
            build_string += 'AddHandler {}\n'.format(handler)

        if self.indices:
            build_string += 'DirectoryIndex {}\n'.format(' '.join(self.indices))

        build_string += 'RewriteEngine {}\n'.format('on' if self.rewrite_engine else 'off')

        build_string += '\n' + '\n'.join(route.build() for route in self.routes)

        return build_string

    def build_config(self) -> str:
        return json.dumps({
                            'template': self.template,
                            'charset':  self.charset,
                            'libraries': [library.value for library in self.libraries]
                        })