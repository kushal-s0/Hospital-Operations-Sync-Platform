from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.user_profile, name='user_profile'),
    path('staff/', views.staff_list, name='staff_list'),
    path('departments/', views.department_list, name='department_list'),
    path('public/doctors/', views.public_doctors_list, name='public_doctors_list'),
]
