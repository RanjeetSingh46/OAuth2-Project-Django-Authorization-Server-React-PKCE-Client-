from django.core.management.base import BaseCommand
from oauth2_provider.models import Application
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create a sample OAuth application (if none exists)'

    def handle(self, *args, **options):
        User = get_user_model()
        admin = User.objects.filter(is_superuser=True).first()
        if not admin:
            self.stdout.write(self.style.ERROR('No superuser found — create one first (python manage.py createsuperuser)'))
            return
        app, created = Application.objects.get_or_create(
            name='Example PKCE Client',
            client_type=Application.CLIENT_PUBLIC,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
            redirect_uris='http://localhost:3000/login',
            user=admin
        )
        self.stdout.write(self.style.SUCCESS(f'Client id: {app.client_id}'))
        self.stdout.write(self.style.SUCCESS(f'Client secret: {getattr(app, "client_secret", "")}'))
