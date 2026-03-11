from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
from core.sitemaps import StaticViewSitemap,BlogSitemap

sitemaps = {
    'static': StaticViewSitemap,
    "blogs": BlogSitemap,


}


urlpatterns = [
    path('', views.home, name='home'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail_page'),
    path('contact/submit/', views.submit_contact, name='submit_contact'),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),

]
