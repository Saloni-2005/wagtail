from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates a superuser if one does not exist'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Check if any superuser exists
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.SUCCESS('Superuser already exists'))
            return
        
        # Create superuser with default credentials
        # CHANGE THESE AFTER FIRST LOGIN!
        username = 'admin'
        email = 'admin@example.com'
        password = 'admin123'  # Change this in production!
        
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        
        self.stdout.write(self.style.SUCCESS(
            f'Superuser created successfully!\n'
            f'Username: {username}\n'
            f'Password: {password}\n'
            f'⚠️  IMPORTANT: Change the password after first login!'
        ))
