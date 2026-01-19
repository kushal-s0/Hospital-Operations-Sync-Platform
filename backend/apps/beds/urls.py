from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, BedViewSet

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'', BedViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
