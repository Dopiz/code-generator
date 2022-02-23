# defaults.py
class {{ service_name }}Config:
    BASE_URL = "https://{{ domain_url }}"

# env.py
class {{ service_name }}Config(defaults.{{ service_name }}Config):
    BASE_URL = "https://{{ domain_url }}"