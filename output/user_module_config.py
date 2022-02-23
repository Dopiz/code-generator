# defaults.py
class UserModuleConfig:
    BASE_URL = "https://api.tests.domain"

# env.py
class UserModuleConfig(defaults.UserModuleConfig):
    BASE_URL = "https://api.tests.domain"