from django.urls import path
from . import admin_views as av

urlpatterns = [
    path('login/', av.admin_login, name='admin_login'),
    path('logout/', av.admin_logout, name='admin_logout'),
    path('', av.dashboard, name='admin_dashboard'),
    path('settings/', av.site_settings, name='admin_site_settings'),
    path('tickers/', av.manage_tickers, name='admin_tickers'),
    path('qualifications/', av.manage_qualifications, name='admin_qualifications'),
    path('certificates/', av.manage_certificates, name='admin_certificates'),
    path('chambers/', av.manage_chambers, name='admin_chambers'),
    path('services/', av.manage_services, name='admin_services'),
    path('fees/', av.manage_fees, name='admin_fees'),
    path('appointments/', av.manage_appointments, name='admin_appointments'),
    path('appointment-details/<int:pk>/', av.appointment_details, name='appointment_details'),
    path('reviews/', av.manage_reviews, name='admin_reviews'),
    path('videos/', av.manage_videos, name='admin_videos'),
    path('blogs/', av.manage_blogs, name='admin_blogs'),
    path('team/', av.manage_team, name='admin_team'),
    path('faqs/', av.manage_faqs, name='admin_faqs'),
    path('messages/', av.manage_messages, name='admin_messages'),
    path('media/', av.manage_media, name='admin_media'),
]
