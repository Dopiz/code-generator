import pytest

from api.{{ s_service_name }} import {{ service_name }}{{ component_name }}API
from dataprocess import DataProcess

data_process = DataProcess("{{ s_service_name }}/{{ s_component_name }}")


class TestCase:

    {{ s_component_name }}_api = {{ service_name }}{{ component_name }}API()
    {% for api in apis %}
    @pytest.mark.parametrize('data', data_process.read_data("{{ api.api_name.lower() }}"))
    def test_{{ api.api_name.lower() }}(self, is_run, data):

        if not is_run(is_run=data.get('is_run'), case_id=data.get('case_id')):
            pytest.skip()

        res = self.{{ s_component_name }}_api.{{ api.api_name.lower() }}(
            {%- for header in api.headers %}
            {{ header.s_name }}=data['{{ header.s_name }}'],
            {%- endfor %}
            {%- for body in api.body %}
            {{ body.s_name }}=data['{{ body.s_name }}'],
            {%- endfor %}
            {%- for param in api.params %}
            {{ param.s_name }}=data['{{ param.s_name }}'],
            {%- endfor %}
        ).json()

        assert res['result'] == data['expected_result']
    {% endfor %}