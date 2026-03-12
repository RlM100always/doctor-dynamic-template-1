from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Count
import json
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from django.utils import timezone
from django.http import JsonResponse

from core.models import (
    SiteSettings, TickerMessage, TrustChip, HeroDegree, AboutHighlight,
    Qualification, Certificate, Chamber, Service, FeeItem, FeeInfo,
    AppointmentSlot, Review, RatingBar, Video, BlogPost, MediaCoverage,
    TeamMember, FAQ, ContactMessage
)
from appointments.models import Appointment


def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def admin_login(request):
    if request.user.is_authenticated and is_admin(request.user):
        return redirect('admin_dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and is_admin(user):
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'ভুল ব্যবহারকারী নাম বা পাসওয়ার্ড।')
    return render(request, 'admin_panel/login.html')


def admin_logout(request):
    logout(request)
    return redirect('admin_login')


@login_required(login_url='/admin-panel/login/')
def dashboard(request):
    if not is_admin(request.user):
        return redirect('admin_login')
    context = {
        'total_appointments': Appointment.objects.count(),
        'pending_appointments': Appointment.objects.filter(status='pending').count(),
        'confirmed_appointments': Appointment.objects.filter(status='confirmed').count(),
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
        'recent_appointments': Appointment.objects.order_by('-created_at')[:5],
        'recent_messages': ContactMessage.objects.order_by('-created_at')[:5],
        'total_reviews': Review.objects.count(),
        'total_blogs': BlogPost.objects.count(),
    }
    return render(request, 'admin_panel/dashboard.html', context)


# ── SITE SETTINGS ──────────────────────────────────────────────────────────────
@login_required(login_url='/admin-panel/login/')
def site_settings(request):
    if not is_admin(request.user):
        return redirect('admin_login')
    obj, _ = SiteSettings.objects.get_or_create(pk=1)
    if request.method == 'POST':
        # Check if this is a HeroDegree action
        hero_action = request.POST.get('hero_action')
        
        if hero_action == 'add_hero_degree':
            HeroDegree.objects.create(
                label=request.POST.get('label'),
                icon_class=request.POST.get('icon_class', 'fas fa-certificate'),
                order=int(request.POST.get('order', 0)),
                is_active=request.POST.get('is_active') == 'on'
            )
            messages.success(request, 'হিরো ডিগ্রি যোগ করা হয়েছে।')
            return redirect('admin_site_settings')
            
        elif hero_action == 'edit_hero_degree':
            hero_id = request.POST.get('hero_id')
            hero = get_object_or_404(HeroDegree, pk=hero_id)
            hero.label = request.POST.get('label')
            hero.icon_class = request.POST.get('icon_class', 'fas fa-certificate')
            hero.order = int(request.POST.get('order', 0))
            hero.is_active = request.POST.get('is_active') == 'on'
            hero.save()
            messages.success(request, 'হিরো ডিগ্রি আপডেট করা হয়েছে।')
            return redirect('admin_site_settings')
            
        elif hero_action == 'delete_hero_degree':
            hero_id = request.POST.get('hero_id')
            HeroDegree.objects.filter(pk=hero_id).delete()
            messages.success(request, 'হিরো ডিগ্রি মুছে ফেলা হয়েছে।')
            return redirect('admin_site_settings')

        obj.doctor_name = request.POST.get('doctor_name', obj.doctor_name)
        obj.doctor_name_en = request.POST.get('doctor_name_en', obj.doctor_name_en)
        obj.specialty = request.POST.get('specialty', obj.specialty)
        obj.degrees = request.POST.get('degrees', obj.degrees)
        obj.bio = request.POST.get('bio', obj.bio)
        obj.phone = request.POST.get('phone', obj.phone)
        obj.phone_raw = request.POST.get('phone_raw', obj.phone_raw)
        obj.whatsapp = request.POST.get('whatsapp', obj.whatsapp)
        obj.email = request.POST.get('email', obj.email)
        obj.facebook_url = request.POST.get('facebook_url', obj.facebook_url)
        obj.youtube_url = request.POST.get('youtube_url', obj.youtube_url)
        obj.profile_photo_url = request.POST.get('profile_photo_url', obj.profile_photo_url)
        obj.years_experience = int(request.POST.get('years_experience', obj.years_experience))
        obj.successful_deliveries = int(request.POST.get('successful_deliveries', obj.successful_deliveries))
        obj.google_rating = request.POST.get('google_rating', obj.google_rating)
        obj.google_review_count = int(request.POST.get('google_review_count', obj.google_review_count))
        obj.research_papers = int(request.POST.get('research_papers', obj.research_papers))
        obj.booking_fee = int(request.POST.get('booking_fee', obj.booking_fee))
        obj.bkash_number = request.POST.get('bkash_number', obj.bkash_number)
        obj.nagad_number = request.POST.get('nagad_number', obj.nagad_number)
        obj.rocket_number = request.POST.get('rocket_number', obj.rocket_number)
        obj.map_embed_url = request.POST.get('map_embed_url', obj.map_embed_url)
        obj.maps_link = request.POST.get('maps_link', obj.maps_link)
        obj.meta_title = request.POST.get('meta_title', obj.meta_title)
        obj.meta_description = request.POST.get('meta_description', obj.meta_description)
        if 'profile_photo' in request.FILES:
            obj.profile_photo = request.FILES['profile_photo']
        obj.save()
        messages.success(request, 'সেটিংস সংরক্ষিত হয়েছে।')
        return redirect('admin_site_settings')
    return render(request, 'admin_panel/site_settings.html', {'obj': obj})


# ── GENERIC CRUD HELPERS ───────────────────────────────────────────────────────
def _list_view(request, model, template, context_name, order_field='order'):
    if not is_admin(request.user):
        return redirect('admin_login')
    items = model.objects.all()
    return render(request, template, {context_name: items})


def _delete_view(request, model, redirect_url):
    if not is_admin(request.user):
        return redirect('admin_login')
    if request.method == 'POST':
        pk = request.POST.get('pk')
        model.objects.filter(pk=pk).delete()
        messages.success(request, 'মুছে ফেলা হয়েছে।')
    return redirect(redirect_url)


# ── TICKER ──────────────────────────────────────────────────────────────────────
@login_required(login_url='/admin-panel/login/')
def manage_tickers(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            TickerMessage.objects.create(
                message=request.POST.get('message'),
                order=request.POST.get('order', 0),
            )
            messages.success(request, 'টিকার যোগ করা হয়েছে।')
        elif action == 'delete':
            TickerMessage.objects.filter(pk=request.POST.get('pk')).delete()
            messages.success(request, 'মুছে ফেলা হয়েছে।')
        elif action == 'toggle':
            obj = TickerMessage.objects.get(pk=request.POST.get('pk'))
            obj.is_active = not obj.is_active
            obj.save()
        return redirect('admin_tickers')
    items = TickerMessage.objects.all()
    return render(request, 'admin_panel/tickers.html', {'items': items})


# ── QUALIFICATIONS ─────────────────────────────────────────────────────────────
@login_required(login_url='/admin-panel/login/')
def manage_qualifications(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        pk = request.POST.get('pk')
        if action == 'add':
            Qualification.objects.create(
                year=request.POST.get('year'),
                degree=request.POST.get('degree'),
                institution=request.POST.get('institution'),
                icon_class=request.POST.get('icon_class', 'fas fa-graduation-cap'),
                entry_type=request.POST.get('entry_type', 'degree'),
                order=request.POST.get('order', 0),
            )
            messages.success(request, 'যোগ্যতা যোগ করা হয়েছে।')
        elif action == 'edit':
            obj = get_object_or_404(Qualification, pk=pk)
            obj.year = request.POST.get('year')
            obj.degree = request.POST.get('degree')
            obj.institution = request.POST.get('institution')
            obj.icon_class = request.POST.get('icon_class', 'fas fa-graduation-cap')
            obj.entry_type = request.POST.get('entry_type', 'degree')
            obj.order = request.POST.get('order', 0)
            obj.save()
            messages.success(request, 'আপডেট হয়েছে।')
        elif action == 'delete':
            Qualification.objects.filter(pk=pk).delete()
            messages.success(request, 'মুছে ফেলা হয়েছে।')
        return redirect('admin_qualifications')
    items = Qualification.objects.all()
    return render(request, 'admin_panel/qualifications.html', {'items': items})


# ── CERTIFICATES ───────────────────────────────────────────────────────────────
@login_required(login_url='/admin-panel/login/')
def manage_certificates(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        pk = request.POST.get('pk')
        if action == 'add':
            Certificate.objects.create(
                number=request.POST.get('number', '01'),
                icon_class=request.POST.get('icon_class', 'fas fa-scroll'),
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                link_text=request.POST.get('link_text', 'সনদ যাচাই করুন'),
                link_url=request.POST.get('link_url', ''),
                is_amber=request.POST.get('is_amber') == 'on',
                order=request.POST.get('order', 0),
            )
            messages.success(request, 'সনদ যোগ করা হয়েছে।')
        elif action == 'edit':
            obj = get_object_or_404(Certificate, pk=pk)
            obj.number = request.POST.get('number', obj.number)
            obj.title = request.POST.get('title')
            obj.description = request.POST.get('description')
            obj.link_text = request.POST.get('link_text')
            obj.link_url = request.POST.get('link_url', '')
            obj.icon_class = request.POST.get('icon_class')
            obj.is_amber = request.POST.get('is_amber') == 'on'
            obj.order = request.POST.get('order', 0)
            obj.save()
            messages.success(request, 'আপডেট হয়েছে।')
        elif action == 'delete':
            Certificate.objects.filter(pk=pk).delete()
            messages.success(request, 'মুছে ফেলা হয়েছে।')
        return redirect('admin_certificates')
    items = Certificate.objects.all()
    return render(request, 'admin_panel/certificates.html', {'items': items})


# ── CHAMBERS ───────────────────────────────────────────────────────────────────
@login_required(login_url='/admin-panel/login/')
def manage_chambers(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        pk = request.POST.get('pk')
        if action == 'add':
            Chamber.objects.create(
                badge=request.POST.get('badge'),
                name=request.POST.get('name'),
                area=request.POST.get('area'),
                address=request.POST.get('address'),
                schedule=request.POST.get('schedule'),
                closed_days=request.POST.get('closed_days'),
                phone=request.POST.get('phone'),
                phone_raw=request.POST.get('phone_raw', ''),
                icon_class=request.POST.get('icon_class', 'fas fa-hospital-alt'),
                is_amber=request.POST.get('is_amber') == 'on',
                order=request.POST.get('order', 0),
            )
            messages.success(request, 'চেম্বার যোগ করা হয়েছে।')
        elif action == 'edit':
            obj = get_object_or_404(Chamber, pk=pk)
            obj.badge = request.POST.get('badge')
            obj.name = request.POST.get('name')
            obj.area = request.POST.get('area')
            obj.address = request.POST.get('address')
            obj.schedule = request.POST.get('schedule')
            obj.closed_days = request.POST.get('closed_days')
            obj.phone = request.POST.get('phone')
            obj.phone_raw = request.POST.get('phone_raw', '')
            obj.icon_class = request.POST.get('icon_class')
            obj.is_amber = request.POST.get('is_amber') == 'on'
            obj.order = request.POST.get('order', 0)
            obj.save()
            messages.success(request, 'আপডেট হয়েছে।')
        elif action == 'delete':
            Chamber.objects.filter(pk=pk).delete()
            messages.success(request, 'মুছে ফেলা হয়েছে।')
        return redirect('admin_chambers')
    items = Chamber.objects.all()
    return render(request, 'admin_panel/chambers.html', {'items': items})


# ── SERVICES ───────────────────────────────────────────────────────────────────
@login_required(login_url='/admin-panel/login/')
def manage_services(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        pk = request.POST.get('pk')
        if action == 'add':
            Service.objects.create(
                icon_class=request.POST.get('icon_class', 'fas fa-stethoscope'),
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                is_featured=request.POST.get('is_featured') == 'on',
                order=request.POST.get('order', 0),
            )
            messages.success(request, 'সেবা যোগ করা হয়েছে।')
        elif action == 'edit':
            obj = get_object_or_404(Service, pk=pk)
            obj.icon_class = request.POST.get('icon_class')
            obj.title = request.POST.get('title')
            obj.description = request.POST.get('description')
            obj.is_featured = request.POST.get('is_featured') == 'on'
            obj.order = request.POST.get('order', 0)
            obj.save()
            messages.success(request, 'আপডেট হয়েছে।')
        elif action == 'delete':
            Service.objects.filter(pk=pk).delete()
            messages.success(request, 'মুছে ফেলা হয়েছে।')
        return redirect('admin_services')
    items = Service.objects.all()
    return render(request, 'admin_panel/services.html', {'items': items})


# ── FEES ────────────────────────────────────────────────────────────────────────
@login_required(login_url='/admin-panel/login/')
def manage_fees(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        pk = request.POST.get('pk')
        if action == 'add':
            FeeItem.objects.create(
                service_name=request.POST.get('service_name'),
                fee=int(request.POST.get('fee', 0)),
                includes=request.POST.get('includes'),
                is_featured=request.POST.get('is_featured') == 'on',
                order=request.POST.get('order', 0),
            )
            messages.success(request, 'ফি যোগ করা হয়েছে।')
        elif action == 'edit':
            obj = get_object_or_404(FeeItem, pk=pk)
            obj.service_name = request.POST.get('service_name')
            obj.fee = int(request.POST.get('fee', 0))
            obj.includes = request.POST.get('includes')
            obj.is_featured = request.POST.get('is_featured') == 'on'
            obj.order = request.POST.get('order', 0)
            obj.save()
            messages.success(request, 'আপডেট হয়েছে।')
        elif action == 'delete':
            FeeItem.objects.filter(pk=pk).delete()
            messages.success(request, 'মুছে ফেলা হয়েছে।')
        return redirect('admin_fees')
    items = FeeItem.objects.all()
    return render(request, 'admin_panel/fees.html', {'items': items})


# ── APPOINTMENTS ───────────────────────────────────────────────────────────────


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta



SORT_WHITELIST = {
    'date', '-date',
    'patient_name', '-patient_name',
    'status', '-status',
    'created_at', '-created_at',
}


@login_required(login_url='/admin-panel/login/')
def manage_appointments(request):

    # ── Filter params ──────────────────────────────────────────────
    status_filter     = request.GET.get('status', '')
    date_range        = request.GET.get('date_range', '')
    date_from         = request.GET.get('date_from', '')
    date_to           = request.GET.get('date_to', '')
    patient_name      = request.GET.get('patient_name', '')
    phone             = request.GET.get('phone', '')
    note_search       = request.GET.get('note_search', '')
    registration_date = request.GET.get('registration_date', '')
    sort_by           = request.GET.get('sort_by', '-date')

    if sort_by not in SORT_WHITELIST:
        sort_by = '-date'

    # ── Handle POST ────────────────────────────────────────────────
    if request.method == 'POST':
        action = request.POST.get('action')
        pk     = request.POST.get('pk')
        obj    = get_object_or_404(Appointment, pk=pk)

        if action == 'status':
            obj.status = request.POST.get('status')
            obj.save()
            messages.success(request, 'স্ট্যাটাস আপডেট হয়েছে।')
        elif action == 'note':
            obj.admin_note = request.POST.get('admin_note', '')
            obj.save()
            messages.success(request, 'নোট সংরক্ষিত হয়েছে।')
        elif action == 'delete':
            obj.delete()
            messages.success(request, 'মুছে ফেলা হয়েছে।')

        url_params = request.GET.urlencode()
        return redirect(
            '{}?{}'.format(request.path, url_params) if url_params else request.path
        )

    # ── Summary (all appointments, no filter) ──────────────────────
    today     = timezone.now().date()
    all_appts = Appointment.objects.all()

    # Status counts for dropdown labels — pure Python dict, no templatetag needed
    raw_counts = dict(
        all_appts.values_list('status').annotate(cnt=Count('id')).values_list('status', 'cnt')
    )

    # Build (value, label, count) tuples — used directly in template
    status_choices_with_counts = [
        (val, label, raw_counts.get(val, 0))
        for val, label in Appointment.STATUS_CHOICES
    ]

    summary = {
        'total':     all_appts.count(),
        'today':     all_appts.filter(date=today).count(),
        'pending':   all_appts.filter(status='pending').count(),
        'confirmed': all_appts.filter(status='confirmed').count(),
        'completed': all_appts.filter(status='completed').count(),
        'cancelled': all_appts.filter(status='cancelled').count(),
    }

    # ── Filtered queryset ──────────────────────────────────────────
    appts = all_appts.order_by(sort_by, '-created_at')

    if status_filter:
        appts = appts.filter(status=status_filter)

    if date_range == 'today':
        appts = appts.filter(date=today)
    elif date_range == 'tomorrow':
        appts = appts.filter(date=today + timedelta(days=1))
    elif date_range == 'yesterday':
        appts = appts.filter(date=today - timedelta(days=1))
    elif date_range == 'this_week':
        week_start = today - timedelta(days=today.weekday())
        appts = appts.filter(date__gte=week_start, date__lte=week_start + timedelta(days=6))
    elif date_range == 'last_week':
        appts = appts.filter(date__gte=today - timedelta(days=7))
    elif date_range == 'this_month':
        appts = appts.filter(date__year=today.year, date__month=today.month)
    elif date_range == 'last_month':
        appts = appts.filter(date__gte=today - timedelta(days=30))
    elif date_range == 'last_year':
        appts = appts.filter(date__gte=today - timedelta(days=365))
    elif date_range == 'custom' and date_from and date_to:
        appts = appts.filter(date__gte=date_from, date__lte=date_to)

    if patient_name:
        appts = appts.filter(patient_name__icontains=patient_name)
    if phone:
        appts = appts.filter(phone__icontains=phone)
    if note_search:
        appts = appts.filter(
            Q(note__icontains=note_search) | Q(admin_note__icontains=note_search)
        )
    if registration_date:
        appts = appts.filter(created_at__date=registration_date)

    total_filtered = appts.count()

    # ── Pagination ──────────────────────────────────────────────────
    paginator   = Paginator(appts, 20)
    page_number = request.GET.get('page')
    page_obj    = paginator.get_page(page_number)

    return render(request, 'admin_panel/appointments.html', {
        'appointments':              page_obj,
        'total_filtered':            total_filtered,
        'summary':                   summary,
        'status_choices_with_counts': status_choices_with_counts,  # (val, label, cnt)
        'status_choices':            Appointment.STATUS_CHOICES,   # for edit modal
        'status_filter':             status_filter,
        'date_range':                date_range,
        'date_from':                 date_from,
        'date_to':                   date_to,
        'patient_name':              patient_name,
        'phone':                     phone,
        'note_search':               note_search,
        'registration_date':         registration_date,
        'sort_by':                   sort_by,
    })


@login_required(login_url='/admin-panel/login/')
def appointment_details(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'admin_panel/appointment_details.html', {
        'appointment': appointment
    })






# ── REVIEWS ────────────────────────────────────────────────────────────────────
@login_required(login_url='/admin-panel/login/')
def manage_reviews(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        pk = request.POST.get('pk')
        if action == 'add':
            Review.objects.create(
                reviewer_name=request.POST.get('reviewer_name'),
                rating=int(request.POST.get('rating', 5)),
                review_text=request.POST.get('review_text'),
                is_verified=request.POST.get('is_verified') == 'on',
                is_accent=request.POST.get('is_accent') == 'on',
                order=request.POST.get('order', 0),
            )
            messages.success(request, 'রিভিউ যোগ করা হয়েছে।')
        elif action == 'edit':
            obj = get_object_or_404(Review, pk=pk)
            obj.reviewer_name = request.POST.get('reviewer_name')
            obj.rating = int(request.POST.get('rating', 5))
            obj.review_text = request.POST.get('review_text')
            obj.is_verified = request.POST.get('is_verified') == 'on'
            obj.is_accent = request.POST.get('is_accent') == 'on'
            obj.order = request.POST.get('order', 0)
            obj.save()
            messages.success(request, 'আপডেট হয়েছে।')
        elif action == 'delete':
            Review.objects.filter(pk=pk).delete()
            messages.success(request, 'মুছে ফেলা হয়েছে।')
        elif action == 'toggle':
            obj = Review.objects.get(pk=pk)
            obj.is_active = not obj.is_active
            obj.save()
        return redirect('admin_reviews')
    items = Review.objects.all()
    return render(request, 'admin_panel/reviews.html', {'items': items})


# ── VIDEOS ─────────────────────────────────────────────────────────────────────
@login_required(login_url='/admin-panel/login/')
def manage_videos(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        pk = request.POST.get('pk')
        if action == 'add':
            Video.objects.create(
                youtube_url=request.POST.get('youtube_url'),
                title=request.POST.get('title'),
                tag=request.POST.get('tag'),
                order=request.POST.get('order', 0),
            )
            messages.success(request, 'ভিডিও যোগ করা হয়েছে।')
        elif action == 'edit':
            obj = get_object_or_404(Video, pk=pk)
            obj.youtube_url = request.POST.get('youtube_url')
            obj.title = request.POST.get('title')
            obj.tag = request.POST.get('tag')
            obj.order = request.POST.get('order', 0)
            obj.save()
            messages.success(request, 'আপডেট হয়েছে।')
        elif action == 'delete':
            Video.objects.filter(pk=pk).delete()
            messages.success(request, 'মুছে ফেলা হয়েছে।')
        return redirect('admin_videos')
    items = Video.objects.all()
    return render(request, 'admin_panel/videos.html', {'items': items})


# ── BLOGS ──────────────────────────────────────────────────────────────────────
@login_required(login_url='/admin-panel/login/')
def manage_blogs(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        pk = request.POST.get('pk')
        if action == 'add':
            BlogPost.objects.create(
                icon_class=request.POST.get('icon_class', 'fas fa-baby'),
                category=request.POST.get('category'),
                title=request.POST.get('title'),
                excerpt=request.POST.get('excerpt'),
                full_content=request.POST.get('full_content', ''),
                is_large=request.POST.get('is_large') == 'on',
                order=request.POST.get('order', 0),
            )
            messages.success(request, 'ব্লগ পোস্ট যোগ করা হয়েছে।')
        elif action == 'edit':
            obj = get_object_or_404(BlogPost, pk=pk)
            obj.icon_class = request.POST.get('icon_class')
            obj.category = request.POST.get('category')
            obj.title = request.POST.get('title')
            obj.excerpt = request.POST.get('excerpt')
            obj.full_content = request.POST.get('full_content', '')
            obj.is_large = request.POST.get('is_large') == 'on'
            obj.order = request.POST.get('order', 0)
            obj.save()
            messages.success(request, 'আপডেট হয়েছে।')
        elif action == 'delete':
            BlogPost.objects.filter(pk=pk).delete()
            messages.success(request, 'মুছে ফেলা হয়েছে।')
        elif action == 'toggle':
            obj = BlogPost.objects.get(pk=pk)
            obj.is_active = not obj.is_active
            obj.save()
        return redirect('admin_blogs')
    items = BlogPost.objects.all()
    return render(request, 'admin_panel/blogs.html', {'items': items})


# ── TEAM ───────────────────────────────────────────────────────────────────────
@login_required(login_url='/admin-panel/login/')
def manage_team(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        pk = request.POST.get('pk')
        if action == 'add':
            member = TeamMember.objects.create(
                role=request.POST.get('role'),
                name=request.POST.get('name'),
                qualifications=request.POST.get('qualifications'),
                photo_url=request.POST.get('photo_url', ''),
                icon_class=request.POST.get('icon_class', 'fas fa-user-md'),
                is_lead=request.POST.get('is_lead') == 'on',
                order=request.POST.get('order', 0),
            )
            if 'photo' in request.FILES:
                member.photo = request.FILES['photo']
                member.save()
            messages.success(request, 'দলের সদস্য যোগ করা হয়েছে।')
        elif action == 'edit':
            obj = get_object_or_404(TeamMember, pk=pk)
            obj.role = request.POST.get('role')
            obj.name = request.POST.get('name')
            obj.qualifications = request.POST.get('qualifications')
            obj.photo_url = request.POST.get('photo_url', '')
            obj.icon_class = request.POST.get('icon_class')
            obj.is_lead = request.POST.get('is_lead') == 'on'
            obj.order = request.POST.get('order', 0)
            if 'photo' in request.FILES:
                obj.photo = request.FILES['photo']
            obj.save()
            messages.success(request, 'আপডেট হয়েছে।')
        elif action == 'delete':
            TeamMember.objects.filter(pk=pk).delete()
            messages.success(request, 'মুছে ফেলা হয়েছে।')
        return redirect('admin_team')
    items = TeamMember.objects.all()
    return render(request, 'admin_panel/team.html', {'items': items})


# ── FAQ ────────────────────────────────────────────────────────────────────────
@login_required(login_url='/admin-panel/login/')
def manage_faqs(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        pk = request.POST.get('pk')
        if action == 'add':
            FAQ.objects.create(
                question=request.POST.get('question'),
                answer=request.POST.get('answer'),
                order=request.POST.get('order', 0),
            )
            messages.success(request, 'FAQ যোগ করা হয়েছে।')
        elif action == 'edit':
            obj = get_object_or_404(FAQ, pk=pk)
            obj.question = request.POST.get('question')
            obj.answer = request.POST.get('answer')
            obj.order = request.POST.get('order', 0)
            obj.save()
            messages.success(request, 'আপডেট হয়েছে।')
        elif action == 'delete':
            FAQ.objects.filter(pk=pk).delete()
            messages.success(request, 'মুছে ফেলা হয়েছে।')
        return redirect('admin_faqs')
    items = FAQ.objects.all()
    return render(request, 'admin_panel/faqs.html', {'items': items})


# ── MESSAGES ───────────────────────────────────────────────────────────────────
@login_required(login_url='/admin-panel/login/')
def manage_messages(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        pk = request.POST.get('pk')
        obj = get_object_or_404(ContactMessage, pk=pk)
        if action == 'read':
            obj.is_read = True
            obj.save()
        elif action == 'delete':
            obj.delete()
            messages.success(request, 'বার্তা মুছে ফেলা হয়েছে।')
        return redirect('admin_messages')
    msgs = ContactMessage.objects.all()
    return render(request, 'admin_panel/messages.html', {'messages_list': msgs})


# ── MEDIA COVERAGE ─────────────────────────────────────────────────────────────
@login_required(login_url='/admin-panel/login/')
def manage_media(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        pk = request.POST.get('pk')
        if action == 'add':
            MediaCoverage.objects.create(
                icon_class=request.POST.get('icon_class', 'fas fa-newspaper'),
                outlet_name=request.POST.get('outlet_name'),
                description=request.POST.get('description'),
                is_amber=request.POST.get('is_amber') == 'on',
                order=request.POST.get('order', 0),
            )
            messages.success(request, 'মিডিয়া কভারেজ যোগ করা হয়েছে।')
        elif action == 'edit':
            obj = get_object_or_404(MediaCoverage, pk=pk)
            obj.icon_class = request.POST.get('icon_class')
            obj.outlet_name = request.POST.get('outlet_name')
            obj.description = request.POST.get('description')
            obj.is_amber = request.POST.get('is_amber') == 'on'
            obj.order = request.POST.get('order', 0)
            obj.save()
            messages.success(request, 'আপডেট হয়েছে।')
        elif action == 'delete':
            MediaCoverage.objects.filter(pk=pk).delete()
            messages.success(request, 'মুছে ফেলা হয়েছে।')
        return redirect('admin_media')
    items = MediaCoverage.objects.all()
    return render(request, 'admin_panel/media.html', {'items': items})


# ── HERO DEGREES ─────────────────────────────────────────────────────────────
@login_required(login_url='/admin-panel/login/')
def manage_hero_degrees(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        pk = request.POST.get('pk')
        
        if action == 'add':
            HeroDegree.objects.create(
                label=request.POST.get('label'),
                order=int(request.POST.get('order', 0)),
                is_active=request.POST.get('is_active') == 'on'
            )
            messages.success(request, 'হিরো ডিগ্রি যোগ করা হয়েছে।')
            
        elif action == 'edit':
            obj = get_object_or_404(HeroDegree, pk=pk)
            obj.label = request.POST.get('label')
            obj.order = int(request.POST.get('order', 0))
            obj.is_active = request.POST.get('is_active') == 'on'
            obj.save()
            messages.success(request, 'হিরো ডিগ্রি আপডেট করা হয়েছে।')
            
        elif action == 'delete':
            HeroDegree.objects.filter(pk=pk).delete()
            messages.success(request, 'হিরো ডিগ্রি মুছে ফেলা হয়েছে।')
            
        elif action == 'toggle':
            obj = HeroDegree.objects.get(pk=pk)
            obj.is_active = not obj.is_active
            obj.save()
            
        return redirect('admin_hero_degrees')
        
    items = HeroDegree.objects.all().order_by('order')
    return render(request, 'admin_panel/hero_degrees.html', {'items': items})


# ── RATING BARS ─────────────────────────────────────────────────────────────
@login_required(login_url='/admin-panel/login/')
def manage_rating_bars(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        pk = request.POST.get('pk')
        
        if action == 'add':
            RatingBar.objects.create(
                stars=int(request.POST.get('stars')),
                percentage=int(request.POST.get('percentage'))
            )
            messages.success(request, 'রেটিং বার যোগ করা হয়েছে।')
            
        elif action == 'edit':
            obj = get_object_or_404(RatingBar, pk=pk)
            obj.stars = int(request.POST.get('stars'))
            obj.percentage = int(request.POST.get('percentage'))
            obj.save()
            messages.success(request, 'রেটিং বার আপডেট করা হয়েছে।')
            
        elif action == 'delete':
            RatingBar.objects.filter(pk=pk).delete()
            messages.success(request, 'রেটিং বার মুছে ফেলা হয়েছে।')
            
        return redirect('admin_rating_bars')
        
    items = RatingBar.objects.all().order_by('-stars')
    return render(request, 'admin_panel/rating_bars.html', {'items': items})


# ── TRUST CHIPS ─────────────────────────────────────────────────────────────
@login_required(login_url='/admin-panel/login/')
def manage_trust_chips(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        pk = request.POST.get('pk')
        
        if action == 'add':
            TrustChip.objects.create(
                icon_class=request.POST.get('icon_class', 'fas fa-award'),
                text=request.POST.get('text'),
                order=int(request.POST.get('order', 0)),
                is_active=request.POST.get('is_active') == 'on'
            )
            messages.success(request, 'ট্রাস্ট চিপ যোগ করা হয়েছে।')
            
        elif action == 'edit':
            obj = get_object_or_404(TrustChip, pk=pk)
            obj.icon_class = request.POST.get('icon_class')
            obj.text = request.POST.get('text')
            obj.order = int(request.POST.get('order', 0))
            obj.is_active = request.POST.get('is_active') == 'on'
            obj.save()
            messages.success(request, 'ট্রাস্ট চিপ আপডেট করা হয়েছে।')
            
        elif action == 'delete':
            TrustChip.objects.filter(pk=pk).delete()
            messages.success(request, 'ট্রাস্ট চিপ মুছে ফেলা হয়েছে।')
            
        elif action == 'toggle':
            obj = TrustChip.objects.get(pk=pk)
            obj.is_active = not obj.is_active
            obj.save()
            
        return redirect('admin_trust_chips')
        
    items = TrustChip.objects.all().order_by('order')
    return render(request, 'admin_panel/trust_chips.html', {'items': items})


# ── ABOUT HIGHLIGHTS ─────────────────────────────────────────────────────────
@login_required(login_url='/admin-panel/login/')
def manage_about_highlights(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        pk = request.POST.get('pk')
        
        if action == 'add':
            AboutHighlight.objects.create(
                icon_class=request.POST.get('icon_class', 'fas fa-graduation-cap'),
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                order=int(request.POST.get('order', 0)),
                is_active=request.POST.get('is_active') == 'on'
            )
            messages.success(request, 'পরিচিতির হাইলাইট যোগ করা হয়েছে।')
            
        elif action == 'edit':
            obj = get_object_or_404(AboutHighlight, pk=pk)
            obj.icon_class = request.POST.get('icon_class')
            obj.title = request.POST.get('title')
            obj.description = request.POST.get('description')
            obj.order = int(request.POST.get('order', 0))
            obj.is_active = request.POST.get('is_active') == 'on'
            obj.save()
            messages.success(request, 'পরিচিতির হাইলাইট আপডেট করা হয়েছে।')
            
        elif action == 'delete':
            AboutHighlight.objects.filter(pk=pk).delete()
            messages.success(request, 'পরিচিতির হাইলাইট মুছে ফেলা হয়েছে।')
            
        elif action == 'toggle':
            obj = AboutHighlight.objects.get(pk=pk)
            obj.is_active = not obj.is_active
            obj.save()
            
        return redirect('admin_about_highlights')
        
    items = AboutHighlight.objects.all().order_by('order')
    return render(request, 'admin_panel/about_highlights.html', {'items': items})


# ── TIME SLOTS (AppointmentSlot) ─────────────────────────────────────────────
@login_required(login_url='/admin-panel/login/')
def manage_time_slots(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        pk = request.POST.get('pk')
        
        if action == 'add':
            AppointmentSlot.objects.create(
                label=request.POST.get('label'),
                value=request.POST.get('value'),
                order=int(request.POST.get('order', 0)),
                is_active=request.POST.get('is_active') == 'on'
            )
            messages.success(request, 'সময় স্লট যোগ করা হয়েছে।')
            
        elif action == 'edit':
            obj = get_object_or_404(AppointmentSlot, pk=pk)
            obj.label = request.POST.get('label')
            obj.value = request.POST.get('value')
            obj.order = int(request.POST.get('order', 0))
            obj.is_active = request.POST.get('is_active') == 'on'
            obj.save()
            messages.success(request, 'সময় স্লট আপডেট করা হয়েছে।')
            
        elif action == 'delete':
            AppointmentSlot.objects.filter(pk=pk).delete()
            messages.success(request, 'সময় স্লট মুছে ফেলা হয়েছে।')
            
        elif action == 'toggle':
            obj = AppointmentSlot.objects.get(pk=pk)
            obj.is_active = not obj.is_active
            obj.save()
            
        return redirect('admin_time_slots')
        
    items = AppointmentSlot.objects.all().order_by('order')
    return render(request, 'admin_panel/time_slots.html', {'items': items})


# ── FEE INFO ────────────────────────────────────────────────────────────────
@login_required(login_url='/admin-panel/login/')
def manage_fee_info(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        pk = request.POST.get('pk')
        
        if action == 'add':
            FeeInfo.objects.create(
                icon_class=request.POST.get('icon_class', 'fas fa-check-circle'),
                text=request.POST.get('text'),
                order=int(request.POST.get('order', 0)),
                is_active=request.POST.get('is_active') == 'on'
            )
            messages.success(request, 'ফি তথ্য যোগ করা হয়েছে।')
            
        elif action == 'edit':
            obj = get_object_or_404(FeeInfo, pk=pk)
            obj.icon_class = request.POST.get('icon_class')
            obj.text = request.POST.get('text')
            obj.order = int(request.POST.get('order', 0))
            obj.is_active = request.POST.get('is_active') == 'on'
            obj.save()
            messages.success(request, 'ফি তথ্য আপডেট করা হয়েছে।')
            
        elif action == 'delete':
            FeeInfo.objects.filter(pk=pk).delete()
            messages.success(request, 'ফি তথ্য মুছে ফেলা হয়েছে।')
            
        elif action == 'toggle':
            obj = FeeInfo.objects.get(pk=pk)
            obj.is_active = not obj.is_active
            obj.save()
            
        return redirect('admin_fee_info')
        
    items = FeeInfo.objects.all().order_by('order')
    return render(request, 'admin_panel/fee_info.html', {'items': items})



# ── ICON LIBRARY ────────────────────────────────────────────────────────────
@login_required(login_url='/admin-panel/login/')
def icon_library(request):
    if not is_admin(request.user):
        return redirect('admin_login')
    
    # Organized list of Font Awesome 5 icons by category
    icons = {
        'Medical & Health': [
            {'name': 'Stethoscope', 'class': 'fas fa-stethoscope'},
            {'name': 'Hospital', 'class': 'fas fa-hospital'},
            {'name': 'Hospital Alt', 'class': 'fas fa-hospital-alt'},
            {'name': 'Clinic Medical', 'class': 'fas fa-clinic-medical'},
            {'name': 'User MD', 'class': 'fas fa-user-md'},
            {'name': 'User Nurse', 'class': 'fas fa-user-nurse'},
            {'name': 'Ambulance', 'class': 'fas fa-ambulance'},
            {'name': 'Heart', 'class': 'fas fa-heart'},
            {'name': 'Heartbeat', 'class': 'fas fa-heartbeat'},
            {'name': 'Pills', 'class': 'fas fa-pills'},
            {'name': 'Tablets', 'class': 'fas fa-tablets'},
            {'name': 'Syringe', 'class': 'fas fa-syringe'},
            {'name': 'Vial', 'class': 'fas fa-vial'},
            {'name': 'Band Aid', 'class': 'fas fa-band-aid'},
            {'name': 'Crutch', 'class': 'fas fa-crutch'},
            {'name': 'First Aid', 'class': 'fas fa-first-aid'},
            {'name': 'Tooth', 'class': 'fas fa-tooth'},
            {'name': 'Bone', 'class': 'fas fa-bone'},
            {'name': 'Lungs', 'class': 'fas fa-lungs'},
            {'name': 'Brain', 'class': 'fas fa-brain'},
            {'name': 'Eye', 'class': 'fas fa-eye'},
            {'name': 'Ear', 'class': 'fas fa-ear-deaf'},
            {'name': 'Microscope', 'class': 'fas fa-microscope'},
            {'name': 'X-Ray', 'class': 'fas fa-x-ray'},
            {'name': 'Procedures', 'class': 'fas fa-procedures'},
            {'name': 'Baby', 'class': 'fas fa-baby'},
            {'name': 'Baby Carriage', 'class': 'fas fa-baby-carriage'},
            {'name': 'Pregnancy', 'class': 'fas fa-pregnancy'},
            {'name': 'Female', 'class': 'fas fa-female'},
            {'name': 'Male', 'class': 'fas fa-male'},
            {'name': 'Weight Scale', 'class': 'fas fa-weight-scale'},
            {'name': 'Thermometer', 'class': 'fas fa-thermometer-half'},
        ],
        
        'Education & Awards': [
            {'name': 'Graduation Cap', 'class': 'fas fa-graduation-cap'},
            {'name': 'Award', 'class': 'fas fa-award'},
            {'name': 'Medal', 'class': 'fas fa-medal'},
            {'name': 'Trophy', 'class': 'fas fa-trophy'},
            {'name': 'Scroll', 'class': 'fas fa-scroll'},
            {'name': 'Certificate', 'class': 'fas fa-certificate'},
            {'name': 'Ribbon', 'class': 'fas fa-ribbon'},
            {'name': 'Star', 'class': 'fas fa-star'},
            {'name': 'Crown', 'class': 'fas fa-crown'},
            {'name': 'Book', 'class': 'fas fa-book'},
            {'name': 'Book Open', 'class': 'fas fa-book-open'},
            {'name': 'Library', 'class': 'fas fa-library'},
            {'name': 'Pen', 'class': 'fas fa-pen'},
            {'name': 'Pen Fancy', 'class': 'fas fa-pen-fancy'},
            {'name': 'Pen Alt', 'class': 'fas fa-pen-alt'},
        ],
        
        'Communication': [
            {'name': 'Phone', 'class': 'fas fa-phone'},
            {'name': 'Phone Alt', 'class': 'fas fa-phone-alt'},
            {'name': 'Envelope', 'class': 'fas fa-envelope'},
            {'name': 'Envelope Open', 'class': 'fas fa-envelope-open'},
            {'name': 'WhatsApp', 'class': 'fab fa-whatsapp'},
            {'name': 'Facebook', 'class': 'fab fa-facebook'},
            {'name': 'Facebook F', 'class': 'fab fa-facebook-f'},
            {'name': 'Messenger', 'class': 'fab fa-facebook-messenger'},
            {'name': 'Twitter', 'class': 'fab fa-twitter'},
            {'name': 'Instagram', 'class': 'fab fa-instagram'},
            {'name': 'YouTube', 'class': 'fab fa-youtube'},
            {'name': 'LinkedIn', 'class': 'fab fa-linkedin'},
            {'name': 'SMS', 'class': 'fas fa-sms'},
            {'name': 'Comment', 'class': 'fas fa-comment'},
            {'name': 'Comments', 'class': 'fas fa-comments'},
            {'name': 'Comment Medical', 'class': 'fas fa-comment-medical'},
        ],
        
        'Business & Location': [
            {'name': 'Building', 'class': 'fas fa-building'},
            {'name': 'Hospital Alt', 'class': 'fas fa-hospital-alt'},
            {'name': 'Clinic', 'class': 'fas fa-clinic-medical'},
            {'name': 'Map Marker', 'class': 'fas fa-map-marker-alt'},
            {'name': 'Map', 'class': 'fas fa-map'},
            {'name': 'Map Pin', 'class': 'fas fa-map-pin'},
            {'name': 'Directions', 'class': 'fas fa-directions'},
            {'name': 'Location', 'class': 'fas fa-location-dot'},
            {'name': 'Clock', 'class': 'fas fa-clock'},
            {'name': 'Calendar', 'class': 'fas fa-calendar'},
            {'name': 'Calendar Alt', 'class': 'fas fa-calendar-alt'},
            {'name': 'Calendar Check', 'class': 'fas fa-calendar-check'},
            {'name': 'Calendar Times', 'class': 'fas fa-calendar-times'},
            {'name': 'Money Bill', 'class': 'fas fa-money-bill'},
            {'name': 'Money Bill Alt', 'class': 'fas fa-money-bill-alt'},
            {'name': 'Credit Card', 'class': 'fas fa-credit-card'},
            {'name': 'Barcode', 'class': 'fas fa-barcode'},
            {'name': 'QR Code', 'class': 'fas fa-qrcode'},
        ],
        
        'Interface & Actions': [
            {'name': 'Check Circle', 'class': 'fas fa-check-circle'},
            {'name': 'Check', 'class': 'fas fa-check'},
            {'name': 'Times Circle', 'class': 'fas fa-times-circle'},
            {'name': 'Times', 'class': 'fas fa-times'},
            {'name': 'Info Circle', 'class': 'fas fa-info-circle'},
            {'name': 'Info', 'class': 'fas fa-info'},
            {'name': 'Exclamation Circle', 'class': 'fas fa-exclamation-circle'},
            {'name': 'Exclamation', 'class': 'fas fa-exclamation'},
            {'name': 'Question Circle', 'class': 'fas fa-question-circle'},
            {'name': 'Question', 'class': 'fas fa-question'},
            {'name': 'Plus Circle', 'class': 'fas fa-plus-circle'},
            {'name': 'Plus', 'class': 'fas fa-plus'},
            {'name': 'Minus Circle', 'class': 'fas fa-minus-circle'},
            {'name': 'Minus', 'class': 'fas fa-minus'},
            {'name': 'Edit', 'class': 'fas fa-edit'},
            {'name': 'Pencil Alt', 'class': 'fas fa-pencil-alt'},
            {'name': 'Trash', 'class': 'fas fa-trash'},
            {'name': 'Trash Alt', 'class': 'fas fa-trash-alt'},
            {'name': 'Save', 'class': 'fas fa-save'},
            {'name': 'Copy', 'class': 'fas fa-copy'},
            {'name': 'Paste', 'class': 'fas fa-paste'},
            {'name': 'Cut', 'class': 'fas fa-cut'},
            {'name': 'Search', 'class': 'fas fa-search'},
            {'name': 'Cog', 'class': 'fas fa-cog'},
            {'name': 'Cogs', 'class': 'fas fa-cogs'},
            {'name': 'Upload', 'class': 'fas fa-upload'},
            {'name': 'Download', 'class': 'fas fa-download'},
        ],
        
        'File & Media': [
            {'name': 'File', 'class': 'fas fa-file'},
            {'name': 'File Alt', 'class': 'fas fa-file-alt'},
            {'name': 'File Medical', 'class': 'fas fa-file-medical'},
            {'name': 'File Medical Alt', 'class': 'fas fa-file-medical-alt'},
            {'name': 'File Pdf', 'class': 'fas fa-file-pdf'},
            {'name': 'File Word', 'class': 'fas fa-file-word'},
            {'name': 'File Excel', 'class': 'fas fa-file-excel'},
            {'name': 'File Image', 'class': 'fas fa-file-image'},
            {'name': 'Image', 'class': 'fas fa-image'},
            {'name': 'Camera', 'class': 'fas fa-camera'},
            {'name': 'Video', 'class': 'fas fa-video'},
            {'name': 'Film', 'class': 'fas fa-film'},
            {'name': 'Play Circle', 'class': 'fas fa-play-circle'},
            {'name': 'Play', 'class': 'fas fa-play'},
            {'name': 'Podcast', 'class': 'fas fa-podcast'},
        ],
        
        'Miscellaneous': [
            {'name': 'Leaf', 'class': 'fas fa-leaf'},
            {'name': 'Seedling', 'class': 'fas fa-seedling'},
            {'name': 'Flask', 'class': 'fas fa-flask'},
            {'name': 'Fire', 'class': 'fas fa-fire'},
            {'name': 'Water', 'class': 'fas fa-water'},
            {'name': 'Shield Alt', 'class': 'fas fa-shield-alt'},
            {'name': 'Shield', 'class': 'fas fa-shield'},
            {'name': 'Lock', 'class': 'fas fa-lock'},
            {'name': 'Lock Open', 'class': 'fas fa-lock-open'},
            {'name': 'Key', 'class': 'fas fa-key'},
            {'name': 'Globe', 'class': 'fas fa-globe'},
            {'name': 'Globe Asia', 'class': 'fas fa-globe-asia'},
            {'name': 'Flag', 'class': 'fas fa-flag'},
            {'name': 'Hand Heart', 'class': 'fas fa-hand-holding-heart'},
            {'name': 'Heart Circle', 'class': 'fas fa-heart-circle'},
            {'name': 'Users', 'class': 'fas fa-users'},
            {'name': 'User Circle', 'class': 'fas fa-user-circle'},
            {'name': 'User', 'class': 'fas fa-user'},
            {'name': 'User Plus', 'class': 'fas fa-user-plus'},
        ],
    }
    
    return render(request, 'admin_panel/icon_library.html', {'categories': icons})