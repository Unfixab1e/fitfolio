import requests
from django.conf import settings

def get_oauth_token(service_name):
    return settings.OAUTH_TOKENS[service_name]

def fetch_google_fit_data():
    url = "https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate"
    headers = {'Authorization': f'Bearer {get_oauth_token("google_fit")}', 'Content-Type': 'application/json'}
    data = {...}
    response = requests.post(url, headers=headers, json=data)
    return response.json() if response.status_code == 200 else response.raise_for_status()

def fetch_samsung_health_data():
    url = "https://api.samsunghealth.com/healthdata"
    headers = {'Authorization': f'Bearer {get_oauth_token("samsung_health")}', 'Content-Type': 'application/json'}
    data = {...}
    response = requests.get(url, headers=headers, json=data)
    return response.json() if response.status_code == 200 else response.raise_for_status()
