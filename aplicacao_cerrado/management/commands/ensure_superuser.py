import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Creates or updates the deployment superuser from environment variables."

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "").strip()
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "").strip()
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "")

        missing = [
            name
            for name, value in (
                ("DJANGO_SUPERUSER_USERNAME", username),
                ("DJANGO_SUPERUSER_EMAIL", email),
                ("DJANGO_SUPERUSER_PASSWORD", password),
            )
            if not value
        ]
        if missing:
            raise CommandError(
                "Configure estas variáveis de ambiente na Vercel: "
                + ", ".join(missing)
            )

        user_model = get_user_model()
        user, created = user_model.objects.get_or_create(
            username=username,
            defaults={"email": email},
        )
        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(update_fields=["email", "is_staff", "is_superuser", "password"])

        action = "criado" if created else "atualizado"
        self.stdout.write(
            self.style.SUCCESS(f"Superusuário '{username}' {action} com sucesso.")
        )
