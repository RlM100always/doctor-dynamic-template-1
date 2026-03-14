from django.urls import path
from . import admin_views as av

urlpatterns = [
    path('login/', av.admin_login, name='admin_login'),
    path('logout/', av.admin_logout, name='admin_logout'),
    path('', av.dashboard, name='admin_dashboard'),
    path('settings/', av.site_settings, name='admin_site_settings'),
    path('tickers/', av.manage_tickers, name='admin_tickers'),
    path('hero-degrees/', av.manage_hero_degrees, name='admin_hero_degrees'),
    path('trust-chips/', av.manage_trust_chips, name='admin_trust_chips'),
    path('about-highlights/', av.manage_about_highlights, name='admin_about_highlights'),
    path('qualifications/', av.manage_qualifications, name='admin_qualifications'),
    path('certificates/', av.manage_certificates, name='admin_certificates'),
    path('chambers/', av.manage_chambers, name='admin_chambers'),
    path('services/', av.manage_services, name='admin_services'),
    path('fees/', av.manage_fees, name='admin_fees'),
    path('fee-info/', av.manage_fee_info, name='admin_fee_info'),
    path('appointments/', av.manage_appointments, name='admin_appointments'),
    path('appointment-details/<int:pk>/', av.appointment_details, name='appointment_details'),
    path('reviews/', av.manage_reviews, name='admin_reviews'),
    path('rating-bars/', av.manage_rating_bars, name='admin_rating_bars'),
    path('videos/', av.manage_videos, name='admin_videos'),
    path('blogs/', av.manage_blogs, name='admin_blogs'),
    path('time-slots/', av.manage_time_slots, name='admin_time_slots'),
    path('team/', av.manage_team, name='admin_team'),
    path('faqs/', av.manage_faqs, name='admin_faqs'),
    path('messages/', av.manage_messages, name='admin_messages'),
    path('media/', av.manage_media, name='admin_media'),
    # New icon library URL
    path('icon-library/', av.icon_library, name='admin_icon_library'),
    path('gallery/', av.manage_gallery, name='admin_gallery'),
    path('gallery/add/', av.gallery_add, name='admin_gallery_add'),
    path('gallery/edit/<int:pk>/', av.gallery_edit, name='admin_gallery_edit'),
    path('gallery/delete/<int:pk>/', av.gallery_delete, name='admin_gallery_delete'),
    
    # Chamber Management
path('chamber/', av.chamber_dashboard, name='chamber_dashboard'),
path('chamber/patients/', av.chamber_patients, name='chamber_patients'),
path('chamber/patients/<int:pk>/', av.chamber_patient_detail, name='chamber_patient_detail'),
path('chamber/visits/', av.chamber_visits, name='chamber_visits'),
path('chamber/payments/', av.chamber_payments, name='chamber_payments'),
path('chamber/prescription/<int:visit_pk>/', av.chamber_prescription, name='chamber_prescription'),
path('chamber/followups/', av.chamber_followups, name='chamber_followups'),
path('chamber/quick/', av.chamber_quick_entry, name='chamber_quick_entry'),
path('chamber/analytics/', av.chamber_analytics, name='chamber_analytics'),
path('chamber/reports/', av.chamber_reports, name='chamber_reports'),
path('chamber/patients/search/', av.chamber_patient_search_ajax, name='chamber_patient_search_ajax'),
# Add to urlpatterns
path('chamber/add-area-ajax/', av.chamber_add_area_ajax, name='chamber_add_area_ajax'),


]