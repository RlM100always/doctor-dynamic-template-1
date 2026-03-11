from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import BlogPost

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return ["home", "submit_contact"]

    def location(self, item):
        return reverse(item)


class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return BlogPost.objects.all()

    def location(self, obj):
        return reverse("blog_detail_page", args=[obj.pk])    