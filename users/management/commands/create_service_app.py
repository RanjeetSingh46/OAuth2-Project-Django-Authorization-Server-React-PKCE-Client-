from django.core.management.base import BaseCommand
from oauth2_provider.models import get_application_model
from django.utils.crypto import get_random_string

Application = get_application_model()

class Command(BaseCommand):
    help = "Create a confidential service application for server-to-server token flows."

    def handle(self, *args, **options):
        client_id = get_random_string(40)
        client_secret = get_random_string(80)
        app, created = Application.objects.get_or_create(
            name="ServiceApp",
            client_id=client_id,
            defaults={
                "client_secret": client_secret,
                "client_type": Application.CLIENT_CONFIDENTIAL,
                "authorization_grant_type": Application.GRANT_PASSWORD,
            }
        )
        if not created:
            # update secret if existing
            app.client_secret = client_secret
            app.client_id = client_id
            app.save()
        self.stdout.write(self.style.SUCCESS(
            f"Service app created/updated.\nclient_id={app.client_id}\nclient_secret={client_secret}"
        ))
