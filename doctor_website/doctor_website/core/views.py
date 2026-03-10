from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages as django_messages
import json

from .models import (
    SiteSettings, TickerMessage, TrustChip, HeroDegree, AboutHighlight,
    Qualification, Certificate, Chamber, Service, FeeItem, FeeInfo,
    AppointmentSlot, Review, RatingBar, Video, BlogPost, MediaCoverage,
    TeamMember, FAQ, ContactMessage
)


def home(request):
    context = {
        'tickers': TickerMessage.objects.filter(is_active=True),
        'trust_chips': TrustChip.objects.filter(is_active=True),
        'hero_degrees': HeroDegree.objects.filter(is_active=True),
        'about_highlights': AboutHighlight.objects.filter(is_active=True),
        'qualifications': Qualification.objects.filter(is_active=True),
        'certificates': Certificate.objects.filter(is_active=True),
        'chambers': Chamber.objects.filter(is_active=True),
        'services': Service.objects.filter(is_active=True),
        'fees': FeeItem.objects.filter(is_active=True),
        'fee_infos': FeeInfo.objects.filter(is_active=True),
        'time_slots': AppointmentSlot.objects.filter(is_active=True),
        'reviews': Review.objects.filter(is_active=True),
        'rating_bars': RatingBar.objects.all(),
        'videos': Video.objects.filter(is_active=True),
        'blog_posts': BlogPost.objects.filter(is_active=True),
        'media_coverages': MediaCoverage.objects.filter(is_active=True),
        'team_members': TeamMember.objects.filter(is_active=True),
        'faqs': FAQ.objects.filter(is_active=True),
    }
    return render(request, 'core/home.html', context)


def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk, is_active=True)
    site = SiteSettings.objects.first()  # যদি SiteSettings থাকে

    context = {
        'post': post,
        'site': site,
    }
    return render(request, 'core/blog_detail.html', context)


@require_POST
def submit_contact(request):
    try:
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        email = data.get('email', '').strip()
        message = data.get('message', '').strip()

        if not name or not phone or not message:
            return JsonResponse({'success': False, 'error': 'সব প্রয়োজনীয় তথ্য দিন।'})

        ContactMessage.objects.create(
            name=name, phone=phone, email=email, message=message
        )
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
