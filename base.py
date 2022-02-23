from __future__ import absolute_import

import os
import re

from jinja2 import Environment, FileSystemLoader


def camel_to_snake(text: str):
    matches = re.finditer('[A-Z]', text)
    contents = []
    last_start = 0
    for it in matches:
        start, end = it.span()
        if start > 0:
            contents.append(text[last_start:start])
        last_start = start
    contents.append(text[last_start:])
    return '_'.join(contents).lower()


class Code:

    template = "code.tpl"
    dest_template = "output/%(path)s"

    def __init__(self, data: dict = None, dist_template: str = None, dist_env: dict = None):
        self.data = data or {}
        self.dest_template = dist_template or self.dest_template
        self.dist_env = dist_env or {}

    def dest(self, env: dict = None):
        env = env or {}
        env.update(self.dist_env)
        return self.dest_template % env


class CodeGenerator:

    def __init__(self, data: dict):
        self.data = data

    def _process(self):
        raise NotImplementedError

    def generate(self):
        for code in self._process():
            yield code


class Template:

    def __init__(self):
        self.loader = FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates'))
        self.env = Environment(loader=self.loader)

    def render(self, template_name, **kwargs):
        template = self.env.get_template(template_name)
        return template.render(**kwargs)

    def render_code(self, code):
        return self.render(code.template, **code.data)
