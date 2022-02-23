import pytest

from api.user_module import UserModuleMemberAPI
from dataprocess import DataProcess

data_process = DataProcess("user_module/member")


class TestCase:

    member_api = UserModuleMemberAPI()
    
    @pytest.mark.parametrize('data', data_process.read_data("login"))
    def test_login(self, is_run, data):

        if not is_run(is_run=data.get('is_run'), case_id=data.get('case_id')):
            pytest.skip()

        res = self.member_api.login(
            phone_number=data['phone_number'],
            platform=data['platform'],
        ).json()

        assert res['result'] == data['expected_result']
    
    @pytest.mark.parametrize('data', data_process.read_data("auth"))
    def test_auth(self, is_run, data):

        if not is_run(is_run=data.get('is_run'), case_id=data.get('case_id')):
            pytest.skip()

        res = self.member_api.auth(
            token=data['token'],
            auth_code=data['auth_code'],
        ).json()

        assert res['result'] == data['expected_result']
    
    @pytest.mark.parametrize('data', data_process.read_data("info"))
    def test_info(self, is_run, data):

        if not is_run(is_run=data.get('is_run'), case_id=data.get('case_id')):
            pytest.skip()

        res = self.member_api.info(
            token=data['token'],
            scope=data['scope'],
        ).json()

        assert res['result'] == data['expected_result']
    