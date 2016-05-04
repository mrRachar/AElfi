from mako import template
from mako.lookup import TemplateLookup

def render(text, directory, display, location):
    lookup = TemplateLookup(directories=[directory[:1]]) # For some reason, cutting the first slash off fixes all
    rendering = template.Template(text, lookup=lookup, uri=location).render(**display)
    return rendering
