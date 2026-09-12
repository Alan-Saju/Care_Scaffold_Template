from rest_framework import serializers

from care.facility.models import Facility
from care_connect.models import Consultation, ConsultationStatus


class ConsultationSerializer(serializers.ModelSerializer):
    facility = serializers.SlugRelatedField(
        queryset=Facility.objects.filter(deleted=False),
        slug_field="external_id",
    )
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Consultation
        fields = (
            "external_id",
            "facility",
            "title",
            "status",
            "scheduled_at",
            "notes",
            "provider_reference",
            "created_by",
            "created_date",
            "modified_date",
        )
        read_only_fields = ("external_id", "created_by", "created_date", "modified_date")

    def validate(self, attrs):
        status = attrs.get("status")
        if status == ConsultationStatus.SCHEDULED and not attrs.get(
            "scheduled_at", getattr(self.instance, "scheduled_at", None)
        ):
            raise serializers.ValidationError(
                {"scheduled_at": "A scheduled consultation needs a scheduled time."}
            )
        return attrs
