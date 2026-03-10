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
    paginator   = Paginator(appts, 10)
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
