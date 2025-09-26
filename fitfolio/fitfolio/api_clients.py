import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import ActivityData, WeightData, SleepData
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

def get_oauth_token(service_name):
    return settings.OAUTH_TOKENS.get(service_name, '')

def get_hcgateway_data(user_id, data_type):
    """
    Fetch data from HCGateway API
    data_type can be: 'steps', 'weight', 'sleepSession'
    """
    hc_gateway_url = getattr(settings, 'HCGATEWAY_API_URL', 'https://api.hcgateway.shuchir.dev')
    
    try:
        response = requests.post(
            f"{hc_gateway_url}/api/fetch/{data_type}",
            json={
                "userid": user_id,
                "queries": [
                    "limit(50)",
                    "orderDesc(start)"
                ]
            },
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"HCGateway API error: {response.status_code} - {response.text}")
            return None
            
    except requests.RequestException as e:
        logger.error(f"Failed to fetch {data_type} from HCGateway: {e}")
        return None

def sync_steps_data(user, hc_user_id):
    """Sync steps data from HCGateway"""
    data = get_hcgateway_data(hc_user_id, 'steps')
    if not data or 'data' not in data:
        return 0
    
    synced_count = 0
    for record in data['data']:
        try:
            # Parse the encrypted data - in real implementation, you'd decrypt it
            # For MVP, we'll assume the data structure includes the needed fields
            record_date = datetime.fromisoformat(record['start'].replace('Z', '+00:00')).date()
            
            # Extract steps count from the decrypted data
            # This is a simplified example - actual implementation would decrypt the data field
            steps_count = record.get('count', 0)  # Placeholder
            
            # Create or update activity data
            activity_data, created = ActivityData.objects.update_or_create(
                user=user,
                date=record_date,
                defaults={
                    'steps': steps_count,
                    'distance': steps_count * 0.0008,  # Rough estimate: 0.8m per step
                    'calories_burned': int(steps_count * 0.04)  # Rough estimate
                }
            )
            
            if created:
                synced_count += 1
                
        except (ValueError, KeyError) as e:
            logger.error(f"Error processing steps record: {e}")
            continue
    
    return synced_count

def sync_weight_data(user, hc_user_id):
    """Sync weight data from HCGateway"""
    data = get_hcgateway_data(hc_user_id, 'weight')
    if not data or 'data' not in data:
        return 0
    
    synced_count = 0
    for record in data['data']:
        try:
            record_date = datetime.fromisoformat(record['start'].replace('Z', '+00:00')).date()
            
            # Extract weight from the decrypted data
            # This is a simplified example - actual implementation would decrypt the data field
            weight_kg = record.get('weight', 0)  # Placeholder
            
            weight_data, created = WeightData.objects.update_or_create(
                user=user,
                date=record_date,
                defaults={'weight': weight_kg}
            )
            
            if created:
                synced_count += 1
                
        except (ValueError, KeyError) as e:
            logger.error(f"Error processing weight record: {e}")
            continue
    
    return synced_count

def sync_sleep_data(user, hc_user_id):
    """Sync sleep data from HCGateway"""
    data = get_hcgateway_data(hc_user_id, 'sleepSession')
    if not data or 'data' not in data:
        return 0
    
    synced_count = 0
    for record in data['data']:
        try:
            record_date = datetime.fromisoformat(record['start'].replace('Z', '+00:00')).date()
            
            # Extract sleep data from the decrypted data
            # This is a simplified example - actual implementation would decrypt the data field
            start_time = datetime.fromisoformat(record['start'].replace('Z', '+00:00'))
            end_time = datetime.fromisoformat(record['end'].replace('Z', '+00:00'))
            total_minutes = int((end_time - start_time).total_seconds() / 60)
            
            sleep_data, created = SleepData.objects.update_or_create(
                user=user,
                date=record_date,
                defaults={
                    'sleep_start': start_time,
                    'sleep_end': end_time,
                    'total_sleep_minutes': total_minutes
                }
            )
            
            if created:
                synced_count += 1
                
        except (ValueError, KeyError) as e:
            logger.error(f"Error processing sleep record: {e}")
            continue
    
    return synced_count

def sync_user_health_data(user_id, hc_user_id):
    """
    Sync all health data for a user from HCGateway
    Returns a summary of synced records
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        logger.error(f"User {user_id} does not exist")
        return None
    
    steps_synced = sync_steps_data(user, hc_user_id)
    weight_synced = sync_weight_data(user, hc_user_id)
    sleep_synced = sync_sleep_data(user, hc_user_id)
    
    summary = {
        'user_id': user_id,
        'hc_user_id': hc_user_id,
        'steps_records': steps_synced,
        'weight_records': weight_synced,
        'sleep_records': sleep_synced,
        'total_records': steps_synced + weight_synced + sleep_synced,
        'synced_at': datetime.now()
    }
    
    logger.info(f"Health data sync completed for user {user_id}: {summary}")
    return summary

# Legacy functions (kept for backward compatibility)
def fetch_google_fit_data():
    """Legacy function - now redirects to HCGateway integration"""
    logger.warning("fetch_google_fit_data is deprecated. Use HCGateway integration instead.")
    return {"status": "deprecated", "message": "Use HCGateway integration"}

def fetch_samsung_health_data():
    """Legacy function - now redirects to HCGateway integration"""
    logger.warning("fetch_samsung_health_data is deprecated. Use HCGateway integration instead.")
    return {"status": "deprecated", "message": "Use HCGateway integration"}
