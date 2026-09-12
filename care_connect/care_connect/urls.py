"""URL routes.

Core mounts this module at /api/care_connect/ via the PLUGIN_APPS loop in
config/urls.py. Do not repeat that prefix here.

Routes under `otp/` are for the patient portal (OTP-authenticated, phone-number scoped).
Keep them read-mostly. See the care-auth-contexts skill.
"""

from django.urls import path
from rest_framework.routers import DefaultRouter

from care_connect.viewsets.consultation import ConsultationViewSet
from care_connect.viewsets.config import ConfigView

router = DefaultRouter()
router.register("consultations", ConsultationViewSet, basename="connect-consultation")

urlpatterns = [
    *router.urls,
    path("config/", ConfigView.as_view(), name="care_connect-config"),
]
