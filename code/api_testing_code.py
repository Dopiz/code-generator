from dataclasses import asdict, dataclass
from typing import List

from base import Code, CodeGenerator, camel_to_snake


@dataclass
class Variable:
    name: str
    s_name: str
    type: str


@dataclass
class ApiItem:
    api_name: str
    path: str
    method: str
    headers: List[Variable] = None
    body: List[Variable] = None
    params: List[Variable] = None


@dataclass
class ServiceItem:
    service_name: str
    s_service_name: str
    component_name: str
    s_component_name: str
    domain_url: str
    component_url: str
    apis: List[ApiItem]


class ComponentApiCode(Code):
    template = "api.tpl"
    dest_template = 'output/%(service_name)s_%(component_name)s_api.py'


class ServiceConfigCode(Code):
    template = "config.tpl"
    dest_template = 'output/%(service_name)s_config.py'


class TestScriptCode(Code):
    template = "tests.tpl"
    dest_template = 'output/test_%(service_name)s_%(component_name)s_api.py'


class ApiCodeGenerator(CodeGenerator):

    def _process(self):
        data = self._process_data()
        yield ComponentApiCode(data)
        yield ServiceConfigCode(data)
        yield TestScriptCode(data)

    def _process_data(self):
        service_item = ServiceItem(
            service_name=self.data['service_name'],
            s_service_name=camel_to_snake(self.data['service_name']),
            component_name=self.data['component'],
            s_component_name=camel_to_snake(self.data['component']),
            domain_url="",
            component_url="",
            apis=[]
        )
        for item in self.data['item']:
            url_parse = item['url'].replace("https://", "").split("/")
            service_item.domain_url, service_item.component_url = url_parse[0], url_parse[1]
            api_path = "/".join(url_parse[2:])
            api_item = ApiItem(
                api_name=camel_to_snake(item['name']),
                path=api_path,
                method=item['method'],
                body=[],
                headers=[],
                params=[]
            )
            for var in item['body']:
                v = Variable(
                    name=var['key'],
                    s_name=camel_to_snake(var['key']),
                    type=var['type'],
                )
                api_item.body.append(v)
            for var in item['headers']:
                v = Variable(
                    name=var['key'],
                    s_name=camel_to_snake(var['key']),
                    type=var['type']
                )
                api_item.headers.append(v)
            for var in item['params']:
                v = Variable(
                    name=var['key'],
                    s_name=camel_to_snake(var['key']),
                    type=var['type']
                )
                api_item.params.append(v)

            service_item.apis.append(api_item)

        return asdict(service_item)
