from mako import template

def render(text, display):
    return template.Template(text).render(**display)