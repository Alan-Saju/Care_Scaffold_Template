from django.conf import settings
from django.db import models

from care.utils.models.base import BaseModel


class ConsultationStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    SCHEDULED = "scheduled", "Scheduled"
    IN_PROGRESS = "in_progress", "In progress"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"


class Consultation(BaseModel):
    facility = models.ForeignKey(
        "facility.Facility",
        on_delete=models.CASCADE,
        related_name="connect_consultations",
    )
    title = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20,
        choices=ConsultationStatus,
        default=ConsultationStatus.DRAFT,
    )
    scheduled_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    provider_reference = models.CharField(max_length=200, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="connect_consultations_created",
    )

    class Meta:
        ordering = ("scheduled_at", "-created_date")

    def __str__(self):
        return self.title
