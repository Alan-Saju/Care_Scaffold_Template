import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Consultation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "external_id",
                    models.UUIDField(
                        db_index=True, default=uuid.uuid4, unique=True
                    ),
                ),
                (
                    "created_date",
                    models.DateTimeField(
                        auto_now_add=True, blank=True, db_index=True, null=True
                    ),
                ),
                (
                    "modified_date",
                    models.DateTimeField(
                        auto_now=True, blank=True, db_index=True, null=True
                    ),
                ),
                ("deleted", models.BooleanField(db_index=True, default=False)),
                (
                    "title",
                    models.CharField(max_length=200),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("draft", "Draft"),
                            ("scheduled", "Scheduled"),
                            ("in_progress", "In progress"),
                            ("completed", "Completed"),
                            ("cancelled", "Cancelled"),
                        ],
                        default="draft",
                        max_length=20,
                    ),
                ),
                ("scheduled_at", models.DateTimeField(blank=True, null=True)),
                ("notes", models.TextField(blank=True)),
                ("provider_reference", models.CharField(blank=True, max_length=200)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="connect_consultations_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "facility",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="connect_consultations",
                        to="facility.facility",
                    ),
                ),
            ],
            options={"ordering": ("scheduled_at", "-created_date")},
        ),
    ]
