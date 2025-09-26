from celery import shared_task
from django.contrib.auth import get_user_model
from .api_clients import sync_user_health_data
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

@shared_task
def sync_health_data_for_user(user_id, hc_user_id):
    """
    Sync health data for a specific user from HCGateway
    """
    try:
        summary = sync_user_health_data(user_id, hc_user_id)
        logger.info(f"Health data sync completed for user {user_id}: {summary}")
        return summary
    except Exception as e:
        logger.error(f"Health data sync failed for user {user_id}: {e}")
        raise

@shared_task
def sync_all_users_health_data():
    """
    Sync health data for all users who have HCGateway user IDs configured
    """
    # In a real implementation, you'd have a UserProfile model with hc_user_id
    # For MVP, we'll create a simple mapping
    users_synced = 0
    errors = []
    
    # This is a placeholder - in production you'd have a proper user mapping
    user_hc_mappings = [
        # (django_user_id, hc_gateway_user_id)
        # Example: (1, "hc_user_123")
    ]
    
    for user_id, hc_user_id in user_hc_mappings:
        try:
            sync_health_data_for_user.delay(user_id, hc_user_id)
            users_synced += 1
        except Exception as e:
            error_msg = f"Failed to queue sync for user {user_id}: {e}"
            logger.error(error_msg)
            errors.append(error_msg)
    
    return {
        'users_queued': users_synced,
        'errors': errors,
        'total_users': len(user_hc_mappings)
    }

# Legacy task (updated to use new system)
@shared_task
def update_health_data():
    """
    Legacy task updated to use HCGateway integration
    """
    logger.info("Running legacy update_health_data task - now using HCGateway")
    return sync_all_users_health_data()
