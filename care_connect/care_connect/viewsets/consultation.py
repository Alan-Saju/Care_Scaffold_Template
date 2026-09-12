from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from care_connect.models import Consultation, ConsultationStatus
from care_connect.serializers import ConsultationSerializer


ALLOWED_TRANSITIONS = {
    ConsultationStatus.DRAFT: {
        ConsultationStatus.DRAFT,
        ConsultationStatus.SCHEDULED,
        ConsultationStatus.CANCELLED,
    },
    ConsultationStatus.SCHEDULED: {
        ConsultationStatus.SCHEDULED,
        ConsultationStatus.IN_PROGRESS,
        ConsultationStatus.CANCELLED,
    },
    ConsultationStatus.IN_PROGRESS: {
        ConsultationStatus.IN_PROGRESS,
        ConsultationStatus.COMPLETED,
        ConsultationStatus.CANCELLED,
    },
    ConsultationStatus.COMPLETED: {ConsultationStatus.COMPLETED},
    ConsultationStatus.CANCELLED: {ConsultationStatus.CANCELLED},
}


class ConsultationViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ConsultationSerializer
    lookup_field = "external_id"

    def get_queryset(self):
        queryset = Consultation.objects.select_related("facility", "created_by")
        facility = self.request.query_params.get("facility")
        if facility:
            queryset = queryset.filter(facility__external_id=facility)
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        consultation = self.get_object()
        next_status = serializer.validated_data.get("status", consultation.status)
        if next_status not in ALLOWED_TRANSITIONS[consultation.status]:
            raise ValidationError(
                {
                    "status": (
                        f"Cannot move a {consultation.get_status_display().lower()} "
                        f"consultation to {next_status.replace('_', ' ')}."
                    )
                }
            )
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        consultation = self.get_object()
        consultation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
