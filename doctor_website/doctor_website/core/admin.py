from django.contrib import admin
from .models import (
    SiteSettings, TickerMessage, TrustChip, HeroDegree, AboutHighlight,
    Qualification, Certificate, Chamber, Service, FeeItem, FeeInfo,
    AppointmentSlot, Review, RatingBar, Video, BlogPost, MediaCoverage,
    TeamMember, FAQ, ContactMessage,ChamberPayment,Area,ChamberPatient,ChamberVisit
)
from .models import GalleryItem

@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    fields = ('title', 'image', 'image_url', 'order', 'is_active')
    help_texts = {
        'image_url': 'শুধুমাত্র তখন ব্যবহার করুন যখন ছবি আপলোড করা সম্ভব নয়।',
    }
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
admin.site.register(Area)
admin.site.register(ChamberPatient)
admin.site.register(ChamberVisit)
admin.site.register(ChamberPayment)

