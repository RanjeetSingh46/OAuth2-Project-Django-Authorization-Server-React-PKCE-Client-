from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Seed demo users (admin and regular)'
    def handle(self, *args, **kwargs):
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin','admin@example.com','adminpass')
            self.stdout.write(self.style.SUCCESS('Created superuser: admin / adminpass'))
        if not User.objects.filter(username='ranjeet').exists():
            u = User.objects.create_user('ranjeet','ranjeet@example.com','ranjeetpass')
            u.role = 'user'
            u.save()
            self.stdout.write(self.style.SUCCESS('Created user: ranjeet / ranjeetpass'))
