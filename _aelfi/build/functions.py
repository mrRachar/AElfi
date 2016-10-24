import re

def string_swap(text: str, s1: str, s2: str) -> str:
    """In cases of ambiguity, put the more complex replacement string first"""
    return s2.join(p.replace(s2, s1) for p in text.split(s1))

def escape_capturegroups(string: str) -> str:
    # DEBUG # print('functions.escape_capturegroups#start', string)
    capturegroups_matcher = re.compile(r'(^|[^\\])\(((?:[^?)](?:[^)\\]|\\.)*?)?)\)')
    while capturegroups_matcher.search(string):
        string = capturegroups_matcher.sub(r'\1(?:\2)', string)
    # DEBUG # print('functions.escape_capturegroups#complete', string)
    return string