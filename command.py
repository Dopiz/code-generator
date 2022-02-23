import codecs
import json
from os import makedirs
from os.path import dirname, exists

import click

from code import ApiCodeGenerator
from base import Template, camel_to_snake


def write(dist, content):
    dir_ = dirname(dist)
    if not exists(dir_):
        makedirs(dir_)
    with codecs.open(dist, 'w', 'utf-8') as f:
        f.write(content)


@click.command()
@click.option('-f', '--doc-file', required=True, help='Api Document json file.')
@click.option('-t', '--templates', default='api', help='CodeGen Template.')
@click.option('-s', '--service-name', default='ServiceName', help='Service Name.')
def generate(doc_file, templates, service_name):

    doc = json.load(open(doc_file))
    doc['service_name'] = service_name
    env = {
        'service_name': camel_to_snake(doc['service_name']).lower(),
        'component_name': camel_to_snake(doc['component']).lower()
    }

    template = Template()
    if templates == "api":
        generator = ApiCodeGenerator(doc)
        for code in generator.generate():
            source = template.render_code(code)
            dest = code.dest(env)
            write(dest, source)
    else:
        print("Template not exist.")


generate()
