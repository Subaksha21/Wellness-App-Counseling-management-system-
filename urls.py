from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('schedule/', views.schedule_appointment, name='schedule_appointment'),
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('edit-appointments/', views.edit_appointment, name='edit_appointments'),

    path('contact_support/', views.contact_support, name='contact_support'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('materials/', views.materials, name='materials'),
    path('materials/download/<int:material_id>/', views.download_material, name='download_material'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

