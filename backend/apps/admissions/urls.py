from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdmissionViewSet

router = DefaultRouter()
# router.register(r'rules', AdmissionRuleViewSet)  # Commented out - AdmissionRule model doesn't exist
router.register(r'', AdmissionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
