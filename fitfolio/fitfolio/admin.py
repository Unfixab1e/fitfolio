from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile, ActivityData, WeightData, SleepData

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

# Register custom UserAdmin
admin.site.register(User, UserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'hc_gateway_user_id', 'sync_enabled', 'last_sync']
    list_filter = ['sync_enabled', 'last_sync']
    search_fields = ['user__username', 'hc_gateway_user_id']

@admin.register(ActivityData)
class ActivityDataAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'steps', 'distance', 'calories_burned']
    list_filter = ['date', 'user']
    search_fields = ['user__username']
    date_hierarchy = 'date'

@admin.register(WeightData)
class WeightDataAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'weight', 'created_at']
    list_filter = ['date', 'user']
    search_fields = ['user__username']
    date_hierarchy = 'date'

@admin.register(SleepData)
class SleepDataAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'total_sleep_hours', 'sleep_quality_score', 'created_at']
    list_filter = ['date', 'user']
    search_fields = ['user__username']
    date_hierarchy = 'date'
    
    def total_sleep_hours(self, obj):
        hours = obj.total_sleep_minutes / 60 if obj.total_sleep_minutes else 0
        return f"{hours:.1f}h"
    total_sleep_hours.short_description = 'Sleep Duration'