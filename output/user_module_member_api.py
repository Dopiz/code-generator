from urllib.parse import urljoin

from base_api import BaseAPI
from configurations import UserModuleConfig


class UserModuleMemberAPI(BaseAPI):

    base_url = urljoin(UserModuleConfig.BASE_URL, "Member/")
    
    LOGIN_PATH = "Login"
    AUTH_PATH = "Auth"
    INFO_PATH = "Info"
    
    def login(self, phone_number: str, platform: int, watting_time: float):
        body = {
            'PhoneNumber': phone_number,
            'Platform': platform,
        }
        return self._send_request(
            method='POST',
            url=urljoin(self.base_url, self.LOGIN_PATH),
            json=body,
            watting_time=watting_time
        )
    
    def auth(self, token: str, auth_code: str, watting_time: float):
        headers = {
            'Token': token,
        }
        body = {
            'AuthCode': auth_code,
        }
        return self._send_request(
            method='POST',
            url=urljoin(self.base_url, self.AUTH_PATH),
            headers=headers,
            json=body,
            watting_time=watting_time
        )
    
    def info(self, token: str, scope: list, watting_time: float):
        headers = {
            'Token': token,
        }
        params = {
            'Scope': scope,
        }
        return self._send_request(
            method='GET',
            url=urljoin(self.base_url, self.INFO_PATH),
            headers=headers,
            params=params,
            watting_time=watting_time
        )
    