from django.urls import path
from .views import DashboardSummaryView, DepartmentSummaryView

urlpatterns = [
    path('summary/', DashboardSummaryView.as_view(), name='dashboard-summary'),
    path('departments/', DepartmentSummaryView.as_view(), name='department-summary'),
]
