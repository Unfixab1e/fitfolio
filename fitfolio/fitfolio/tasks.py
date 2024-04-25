from celery import shared_task
from .api_clients import fetch_google_fit_data, fetch_samsung_health_data

@shared_task
def update_health_data():
    fetch_google_fit_data()
    fetch_samsung_health_data()
