from django.contrib import admin
from .models import (
    SiteSettings, TickerMessage, TrustChip, HeroDegree, AboutHighlight,
    Qualification, Certificate, Chamber, Service, FeeItem, FeeInfo,
    AppointmentSlot, Review, RatingBar, Video, BlogPost, MediaCoverage,
    TeamMember, FAQ, ContactMessage
)

admin.site.register(SiteSettings)
admin.site.register(TickerMessage)
admin.site.register(TrustChip)
admin.site.register(HeroDegree)
admin.site.register(AboutHighlight)
admin.site.register(Qualification)
admin.site.register(Certificate)
admin.site.register(Chamber)
admin.site.register(Service)
admin.site.register(FeeItem)
admin.site.register(FeeInfo)
admin.site.register(AppointmentSlot)
admin.site.register(Review)
admin.site.register(RatingBar)
admin.site.register(Video)
admin.site.register(BlogPost)
admin.site.register(MediaCoverage)
admin.site.register(TeamMember)
admin.site.register(FAQ)
admin.site.register(ContactMessage)
