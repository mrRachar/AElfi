from mako import template
from mako.lookup import TemplateLookup
import os

def render(text, directory, display, location):
    lookup = TemplateLookup(directories=['/']) #[directory+'/']) # For some reason, cutting the first slash off fixes allcontents
    normal_dir = os.getcwd()
    os.chdir(directory)
    text = "<%! from builtins import request, response %>\\\n" + text # C.O.M. availibilty in module level code blocks
    rendering = template.Template(text, lookup=lookup, uri=location).render(**display)
    os.chdir(normal_dir)
    return rendering
