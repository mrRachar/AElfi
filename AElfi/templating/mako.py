from mako import template
from mako.lookup import TemplateLookup

def render(text, directory, display, location):
    lookup = TemplateLookup(directories=[directory[:1]]) # For some reason, cutting the first slash off fixes all
    text = "<%! from builtins import request, response %>\\\n" + text # C.O.M. availibilty in module level code blocks
    rendering = template.Template(text, lookup=lookup, uri=location).render(**display)
    return rendering
