from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OPDQueueViewSet, OPDStatisticsViewSet, AppointmentViewSet, predict_wait_time, public_book_appointment

router = DefaultRouter()
router.register(r'queue', OPDQueueViewSet)
router.register(r'statistics', OPDStatisticsViewSet)
router.register(r'appointments', AppointmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    # ML Wait Time Prediction Endpoint
    path('predict-wait-time/', predict_wait_time, name='predict-wait-time'),
    
    # Public Appointment Booking Endpoint
    path('public/book-appointment/', public_book_appointment, name='public-book-appointment'),
]
