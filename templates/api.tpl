from urllib.parse import urljoin

from base_api import BaseAPI
from configurations import {{ service_name }}Config


class {{ service_name }}{{ component_name }}API(BaseAPI):

    base_url = urljoin({{ service_name }}Config.BASE_URL, "{{ component_url }}/")
    {% for api in apis %}
    {{ api.api_name.upper() }}_PATH = "{{ api.path }}"
    {%- endfor %}
    {% for api in apis %}
    def {{ api.api_name.lower() }}(self, {% for header in api.headers -%}{{ header.s_name }}: {{ header.type }}, {% endfor -%}
    {%- for body in api.body -%}{{ body.s_name }}: {{ body.type }}, {% endfor -%}
    {%- for param in api.params -%}{{ param.s_name }}: {{ param.type }}, {% endfor -%}
    watting_time: float):
        {%- if api.headers %}
        headers = {
            {%- for header in api.headers %}
            '{{ header.name }}': {{ header.s_name }},
            {%- endfor %}
        }
        {%- endif %}
        {%- if api.body %}
        body = {
            {%- for body in api.body %}
            '{{ body.name }}': {{ body.s_name }},
            {%- endfor %}
        }
        {%- endif %}
        {%- if api.params %}
        params = {
            {%- for param in api.params %}
            '{{ param.name }}': {{ param.s_name }},
            {%- endfor %}
        }
        {%- endif %}
        return self._send_request(
            method='{{ api.method }}',
            url=urljoin(self.base_url, self.{{ api.api_name.upper() }}_PATH)
            {%- if api.headers -%},
            headers=headers
            {%- endif %}
            {%- if api.body -%},
            json=body
            {%- endif %}
            {%- if api.params -%},
            params=params
            {%- endif %},
            watting_time=watting_time
        )
    {% endfor -%}
