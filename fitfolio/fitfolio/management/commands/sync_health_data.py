from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from fitfolio.models import UserProfile
from fitfolio.tasks import sync_health_data_for_user, sync_all_users_health_data
from django.utils import timezone

User = get_user_model()

class Command(BaseCommand):
    help = 'Sync health data from HCGateway for users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user',
            type=str,
            help='Sync data for specific user (username)',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Sync data for all users with HCGateway integration enabled',
        )
        parser.add_argument(
            '--setup-user',
            type=str,
            nargs=2,
            metavar=('username', 'hc_user_id'),
            help='Setup HCGateway integration for a user',
        )

    def handle(self, *args, **options):
        if options['setup_user']:
            username, hc_user_id = options['setup_user']
            self.setup_user(username, hc_user_id)
        elif options['user']:
            self.sync_user(options['user'])
        elif options['all']:
            self.sync_all_users()
        else:
            self.stdout.write(
                self.style.ERROR(
                    'Please specify --user <username>, --all, or --setup-user <username> <hc_user_id>'
                )
            )

    def setup_user(self, username, hc_user_id):
        """Setup HCGateway integration for a user"""
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f'User "{username}" does not exist.')

        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.hc_gateway_user_id = hc_user_id
        profile.sync_enabled = True
        profile.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Created profile and enabled HCGateway sync for user "{username}" with HCGateway ID "{hc_user_id}"'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Updated HCGateway sync settings for user "{username}" with HCGateway ID "{hc_user_id}"'
                )
            )

    def sync_user(self, username):
        """Sync health data for a specific user"""
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f'User "{username}" does not exist.')

        try:
            profile = user.profile
            if not profile.sync_enabled:
                raise CommandError(f'HCGateway sync is not enabled for user "{username}"')
            if not profile.hc_gateway_user_id:
                raise CommandError(f'No HCGateway user ID configured for user "{username}"')
        except UserProfile.DoesNotExist:
            raise CommandError(f'No user profile exists for "{username}". Use --setup-user first.')

        self.stdout.write(f'Syncing health data for user "{username}"...')
        
        # Run sync task
        result = sync_health_data_for_user(user.id, profile.hc_gateway_user_id)
        
        if result:
            profile.last_sync = timezone.now()
            profile.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully synced {result["total_records"]} records for user "{username}": '
                    f'{result["steps_records"]} activity, {result["weight_records"]} weight, {result["sleep_records"]} sleep'
                )
            )
        else:
            self.stdout.write(
                self.style.ERROR(f'Failed to sync data for user "{username}"')
            )

    def sync_all_users(self):
        """Sync health data for all users with sync enabled"""
        enabled_profiles = UserProfile.objects.filter(
            sync_enabled=True,
            hc_gateway_user_id__isnull=False
        ).exclude(hc_gateway_user_id='')

        if not enabled_profiles.exists():
            self.stdout.write(
                self.style.WARNING(
                    'No users found with HCGateway sync enabled. Use --setup-user to configure users first.'
                )
            )
            return

        self.stdout.write(f'Found {enabled_profiles.count()} users to sync...')
        
        successful_syncs = 0
        for profile in enabled_profiles:
            try:
                self.stdout.write(f'Syncing user "{profile.user.username}"...')
                result = sync_health_data_for_user(profile.user.id, profile.hc_gateway_user_id)
                
                if result:
                    profile.last_sync = timezone.now()
                    profile.save()
                    successful_syncs += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'  Synced {result["total_records"]} records'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(f'  Failed to sync user "{profile.user.username}"')
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'  Error syncing user "{profile.user.username}": {e}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Sync completed. Successfully synced {successful_syncs}/{enabled_profiles.count()} users.'
            )
        )