from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail_page'),
    path('contact/submit/', views.submit_contact, name='submit_contact'),
]
