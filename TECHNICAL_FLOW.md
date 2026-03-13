# 🔄 Doctor Nish - Technical Flow & Examples

## A. REQUEST FLOW - Step by Step

### Example 1: User Views Homepage

**REQUEST:**
```
User opens browser → Types website URL → Presses Enter
HTTP GET /
```

**DJANGO PROCESSING:**
```
1. URL Router (config/urls.py)
   └─ Matches "/" to core.urls
      └─ Matches "/" to views.home

2. views.home() EXECUTES:
   
   def home(request):
       site = SiteSettings.objects.first()               # Gets doctor info
       context = {
           'site': site,
           'tickers': TickerMessage.objects.filter(is_active=True),
           'trust_chips': TrustChip.objects.filter(is_active=True),
           'hero_degrees': HeroDegree.objects.filter(is_active=True),
           'qualifications': Qualification.objects.filter(is_active=True),
           'certificates': Certificate.objects.filter(is_active=True),
           'chambers': Chamber.objects.filter(is_active=True),
           'services': Service.objects.filter(is_active=True),
           'fees': FeeItem.objects.filter(is_active=True),
           'reviews': Review.objects.filter(is_active=True),
           'videos': Video.objects.filter(is_active=True),
           'blog_posts': BlogPost.objects.filter(is_active=True),
           'team_members': TeamMember.objects.filter(is_active=True),
           'faqs': FAQ.objects.filter(is_active=True),
           'gallery_items': GalleryItem.objects.filter(is_active=True),
           # ... 15+ database queries
       }
       return render(request, 'core/home.html', context)

3. TEMPLATE RENDERING (core/home.html):
   - Accesses context variables
   - {% for item in tickers %} → Loops through announcements
   - {% for item in qualifications %} → Loops through education
   - {{ site.doctor_name }} → Displays doctor name
   - {% if services %} → Conditional sections
   - {% include 'components/gallery.html' %} → Includes sections

4. DATABASE QUERIES:
   Database receives 15+ SELECT queries
   ↓
   Returns data for all sections
   ↓
   Context populated with data

5. HTML GENERATION:
   Template engine combines HTML + context
   ↓
   Returns complete HTML page

6. HTTP RESPONSE:
   Browser receives 200 OK + HTML
   ↓
   Browser renders, loads CSS/JavaScript
   ↓
   User sees beautifully styled homepage
```

**DATABASE QUERIES EXECUTED:**
```sql
SELECT * FROM core_sitesettings LIMIT 1;
SELECT * FROM core_tickermessage WHERE is_active=TRUE ORDER BY order;
SELECT * FROM core_trustchip WHERE is_active=TRUE ORDER BY order;
SELECT * FROM core_herodegree WHERE is_active=TRUE ORDER BY order;
SELECT * FROM core_qualification WHERE is_active=TRUE ORDER BY order;
SELECT * FROM core_certificate WHERE is_active=TRUE ORDER BY order;
SELECT * FROM core_chamber WHERE is_active=TRUE ORDER BY order;
SELECT * FROM core_service WHERE is_active=TRUE ORDER BY order;
SELECT * FROM core_feeitem WHERE is_active=TRUE ORDER BY order;
SELECT * FROM core_review WHERE is_active=TRUE ORDER BY order;
SELECT * FROM core_video WHERE is_active=TRUE ORDER BY order;
SELECT * FROM core_blogpost WHERE is_active=TRUE ORDER BY order;
SELECT * FROM core_galleryitem WHERE is_active=TRUE ORDER BY order;
SELECT * FROM core_faq WHERE is_active=TRUE ORDER BY order;
SELECT * FROM core_teamMember WHERE is_active=TRUE ORDER BY order;
```

---

### Example 2: Patient Books Appointment (AJAX)

**CLIENT-SIDE (JavaScript in browser):**
```javascript
// User fills form: name, phone, date, time_slot, note

document.getElementById('bookBtn').addEventListener('click', function() {
    const data = {
        name: document.getElementById('name').value,
        phone: document.getElementById('phone').value,
        date: document.getElementById('date').value,
        time_slot: document.getElementById('slot').value,
        note: document.getElementById('note').value
    };
    
    // Validate
    if (!data.name || !data.phone) {
        alert('Fill required fields');
        return;
    }
    
    // Send AJAX POST request
    fetch('/appointments/book/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Appointment booked! ID: ' + data.id);
        } else {
            alert('Error: ' + data.error);
        }
    });
});
```

**DJANGO BACKEND:**
```python
# URL routing
# POST /appointments/book/ → views.book_appointment

# appointments/views.py
@require_POST
def book_appointment(request):
    try:
        data = json.loads(request.body)
        
        # Data extraction & validation
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        date = data.get('date', '').strip()
        time_slot = data.get('time_slot', '').strip()
        note = data.get('note', '').strip()
        
        if not name or not phone or not date or not time_slot:
            return JsonResponse({
                'success': False,
                'error': 'সব প্রয়োজনীয় তথ্য দিন।'
            })
        
        # Database insert
        appt = Appointment.objects.create(
            patient_name=name,
            phone=phone,
            date=date,
            time_slot=time_slot,
            note=note,
            status='pending'  # Default status
        )
        
        # Return success response
        return JsonResponse({
            'success': True,
            'id': appt.pk,
            'message': 'অ্যাপয়েন্টমেন্ট বুক হয়েছে!'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })
```

**DATABASE OPERATION:**
```sql
INSERT INTO appointments_appointment 
    (patient_name, phone, date, time_slot, note, status, created_at, updated_at)
VALUES 
    ('Fatima Ahmed', '01811223344', '2026-03-15', '10:00 AM', '', 'pending', NOW(), NOW());

-- Returns ID: 1
```

**RESPONSE TO CLIENT:**
```json
{
    "success": true,
    "id": 1,
    "message": "অ্যাপয়েন্টমেন্ট বুক হয়েছে!"
}
```

**USER SEES:**
```
✅ SUCCESS! Your appointment is confirmed.
   Appointment ID: 1
   Doctor will contact you at 01811223344
```

---

### Example 3: Doctor Logs Into Admin Panel

**CLIENT-SIDE:**
```
User opens browser
↓
Navigates to /admin-panel/login/
↓
Form displayed:
┌─────────────────┐
│ Username: ____  │
│ Password: ____  │
│   [Login]       │
└─────────────────┘
↓
User enters: admin / admin123
↓
Form submits (POST /admin-panel/login/)
```

**DJANGO BACKEND:**
```python
# config/urls.py
path('admin-panel/', include('core.admin_urls')),

# core/admin_urls.py
path('login/', admin_login, name='admin_login'),

# core/admin_views.py
def admin_login(request):
    if request.user.is_authenticated and is_admin(request.user):
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Django's built-in authentication
        user = authenticate(request, username=username, password=password)
        
        if user:
            # Check if admin
            if user.is_staff or user.is_superuser:
                login(request, user)  # Creates session
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Admin সুবিধা নেই।')
        else:
            messages.error(request, 'ভুল ব্যবহারকারী নাম বা পাসওয়ার্ড।')
    
    return render(request, 'admin_panel/login.html')
```

**DATABASE CHECK:**
```sql
SELECT * FROM auth_user WHERE username='admin';
-- Checks if user exists and password matches (hashed)
```

**SESSION CREATION:**
```python
# Django creates session
request.session['_auth_user_id'] = user.id
request.session['_auth_user_backend'] = 'django.contrib.auth.backends.ModelBackend'
request.session['_auth_user_hash'] = user.get_session_auth_hash()
# Session stored in database
```

**REDIRECT:**
```
Browser redirected to /admin-panel/
↓
Dashboard loads
↓
Shows:
- Total Appointments
- Pending Appointments
- Recent Appointments
- Recent Messages
- Stats
```

---

### Example 4: Doctor Views & Edits an Appointment

**REQUEST:**
```
Doctor in admin panel
↓
Clicks "Appointments"
↓
Navigates to GET /admin-panel/appointments/
```

**BACKEND PROCESSING:**
```python
@login_required(login_url='/admin-panel/login/')
def appointments_list(request):
    if not is_admin(request.user):
        return redirect('admin_login')
    
    # Get all appointments
    appointments = Appointment.objects.all().order_by('-created_at')
    
    # Pagination
    paginator = Paginator(appointments, 10)  # 10 per page
    page = request.GET.get('page', 1)
    appointments = paginator.get_page(page)
    
    context = {
        'appointments': appointments,
        'total': Appointment.objects.count(),
        'pending': Appointment.objects.filter(status='pending').count(),
        'confirmed': Appointment.objects.filter(status='confirmed').count(),
    }
    return render(request, 'admin_panel/appointments.html', context)
```

**TEMPLATE DISPLAY:**
```html
<!-- admin_panel/appointments.html -->
<table>
  <tr>
    <th>রোগীর নাম</th>
    <th>ফোন</th>
    <th>তারিখ</th>
    <th>সময়</th>
    <th>স্ট্যাটাস</th>
    <th>অ্যাকশন</th>
  </tr>
  {% for appt in appointments %}
  <tr>
    <td>{{ appt.patient_name }}</td>
    <td>{{ appt.phone }}</td>
    <td>{{ appt.date }}</td>
    <td>{{ appt.time_slot }}</td>
    <td><span class="{{ appt.get_status_badge_class }}">{{ appt.get_status_display }}</span></td>
    <td>
      <a href="/admin-panel/appointments/{{ appt.id }}/edit/">Edit</a>
      <a href="/admin-panel/appointments/{{ appt.id }}/delete/">Delete</a>
    </td>
  </tr>
  {% endfor %}
</table>
```

**DOCTOR CLICKS EDIT:**
```
Navigates to: GET /admin-panel/appointments/1/edit/
↓
Backend fetches appointment
↓
Returns form with current data pre-filled
↓
Doctor changes status: 'pending' → 'confirmed'
↓
Doctor adds note: "রোগী আসবেন আগামীকাল ১০টায়"
↓
Doctor clicks Save
↓
POST /admin-panel/appointments/1/edit/
```

**BACKEND UPDATE:**
```python
@login_required
def edit_appointment(request, appt_id):
    if not is_admin(request.user):
        return redirect('admin_login')
    
    appt = get_object_or_404(Appointment, id=appt_id)
    
    if request.method == 'POST':
        # Update fields
        appt.patient_name = request.POST.get('patient_name')
        appt.phone = request.POST.get('phone')
        appt.status = request.POST.get('status')  # pending/confirmed/completed/cancelled
        appt.admin_note = request.POST.get('admin_note')
        appt.save()
        
        messages.success(request, 'অ্যাপয়েন্টমেন্ট আপডেট হয়েছে।')
        return redirect('appointments_list')
    
    return render(request, 'admin_panel/appointment_form.html', {'appt': appt})
```

**DATABASE UPDATE:**
```sql
UPDATE appointments_appointment
SET 
    status='confirmed',
    admin_note='রোগী আসবেন আগামীকাল ১০টায়',
    updated_at=NOW()
WHERE id=1;
```

**CONFIRMATION:**
```
Doctor sees: "অ্যাপয়েন্টমেন্ট আপডেট হয়েছে।"
↓
Redirected back to appointments list
↓
List now shows updated appointment with status "confirmed"
```

---

## B. CONTEXT PROCESSORS - Global Data Available

**Every template automatically has access to `site` object:**

```python
# core/context_processors.py
def site_settings(request):
    settings = SiteSettings.objects.first()
    return {'site': settings}
```

**In any template:**
```html
<!-- base.html -->
<nav>
    <h1>{{ site.doctor_name }}</h1>          <!-- ডাঃ সানজিদা ইসলাম চৌধুরী -->
    <span>{{ site.specialty }}</span>         <!-- গাইনী ও প্রসূতি বিশেষজ্ঞ -->
    <a href="tel:{{ site.phone_raw }}">
        {{ site.phone }}                       <!-- ০১৮১১-২২৩৩৪৪ -->
    </a>
</nav>
```

---

## C. MIDDLEWARE & SECURITY FLOW

```
Incoming Request
  ↓
SecurityMiddleware (HTTPS)
  ↓
SessionMiddleware (Session data)
  ↓
CommonMiddleware (Basic checks)
  ↓
CsrfViewMiddleware ← CHECKS CSRF TOKEN for POST/PUT/DELETE
  ↓
AuthenticationMiddleware (Load user)
  ↓
MessageMiddleware (Flash messages)
  ↓
View Layer (admin_views.py)
  ├─ @login_required decorator (checks session)
  ├─ is_admin() function (checks staff/superuser)
  └─ Business logic
  ↓
Response
  ↓
Template Rendering
  ↓
HTTP Response
  ↓
Outgoing to Browser
```

---

## D. ORM QUERIES - Examples

### Getting Homepage Data:
```python
# Single simple query:
site = SiteSettings.objects.first()

# Multiple filtered queries:
services = Service.objects.filter(is_active=True).order_by('order')
qualifications = Qualification.objects.filter(is_active=True).order_by('order')

# Counting records:
total_reviews = Review.objects.count()
pending_appointments = Appointment.objects.filter(status='pending').count()

# Complex filtering:
active_chambers = Chamber.objects.filter(
    is_active=True
).values('name', 'schedule', 'phone')

# Pagination:
from django.core.paginator import Paginator
all_appointments = Appointment.objects.order_by('-created_at')
paginator = Paginator(all_appointments, 10)
page_obj = paginator.get_page(request.GET.get('page'))
```

---

## E. TEMPLATE TAGS & FILTERS

```html
<!-- Loop through items -->
{% for item in items %}
    {{ item.title }}
    {% if item.is_active %}
        <span class="badge">Active</span>
    {% endif %}
{% endfor %}

<!-- Count display -->
{% if videos %}
    {{ videos|length }} ভিডিও পাওয়া গেছে
{% endif %}

<!-- String filters -->
{{ blog_post.title|truncatewords:5 }}
{{ doctor_name|upper }}

<!-- Date filters -->
{{ appointment.created_at|date:"d/m/Y" }}

<!-- Custom template tag -->
{% load app_tags %}
{% display_rating review.rating %}
```

---

## F. URL PATTERN MATCHING

```python
# config/urls.py
urlpatterns = [
    path('', include('core.urls')),                    # Public site paths
    path('appointments/', include('appointments.urls')), # Booking paths
    path('admin-panel/', include('core.admin_urls')),  # Admin paths
]

# core/urls.py
urlpatterns = [
    path('', views.home, name='home'),                 # GET /
    path('blog/<int:pk>/', views.blog_detail),         # GET /blog/5/
    path('contact/submit/', views.submit_contact),     # POST /contact/submit/
]

# core/admin_urls.py
urlpatterns = [
    path('login/', admin_login, name='admin_login'),
    path('', dashboard, name='admin_dashboard'),
    path('appointments/', appointments_list),
    # ... 50+ more paths
]

# appointments/urls.py
urlpatterns = [
    path('book/', views.book_appointment),             # POST /appointments/book/
]
```

**URL Resolution Example:**
```
Request: GET /blog/5/
↓
config/urls.py checks patterns in order
↓
Matches: path('', include('core.urls'))
↓
core/urls.py gets remaining: blog/5/
↓
Matches: path('blog/<int:pk>/', views.blog_detail)
↓
pk = 5
↓
Calls: views.blog_detail(request, pk=5)
↓
BlogPost.objects.get(pk=5)
↓
Returns blog post with ID 5
```

---

## G. STATIC FILES & MEDIA SERVING

```python
# settings.py
STATIC_URL = '/static/'                          # URL path
STATICFILES_DIRS = [BASE_DIR / 'static']         # Where files are
STATIC_ROOT = BASE_DIR / 'staticfiles'           # Where collected to

MEDIA_URL = '/media/'                            # URL path
MEDIA_ROOT = BASE_DIR / 'media'                  # Where files stored

# config/urls.py
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

**Request for image:**
```
Browser: GET /media/doctor/dr-sanjida.jpg
↓
Django serves from: media/doctor/dr-sanjida.jpg
↓
File sent to browser
```

---

## H. DATABASE SCHEMA SUMMARY

```sql
-- SiteSettings (Master Config - 1 record)
doctor_nish
├── core_sitesettings
│   ├── id
│   ├── doctor_name
│   ├── phone, email, whatsapp
│   ├── profile_photo (ImageField)
│   ├── booking_fee
│   ├── payment methods

-- Content Models (Multiple records)
├── core_qualification          (20+ records)
├── core_certificate            (5+ records)
├── core_chamber                (2-3 records)
├── core_service                (10+ records)
├── core_feeitem                (8+ records)
├── core_review                 (50+ records)
├── core_video                  (20+ records)
├── core_blogpost               (30+ records)
├── core_teamMember             (5+ records)
├── core_faq                    (10+ records)
├── core_galleryitem            (100+ photos)
├── core_tickermessage          (3-5 records)
├── core_featuredtrust          (5+ records)
├── core_herodegree             (3-4 records)
├── core_aboutHighlight         (4-5 records)
├── core_reatingbar             (5 records - stars 1-5)
├── core_mediacoverage          (10+ records)
├── core_feeinfo                (3-5 records)
├── core_appointmentslot        (8 records)
├── core_contactmessage         (100+ records)

-- Appointment Booking
└── appointments_appointment    (1000+ records)
    ├── id
    ├── patient_name
    ├── phone
    ├── date, time_slot
    ├── status (pending/confirmed/completed/cancelled)
    ├── created_at, updated_at
```

---

Perfect! This comprehensive overview covers the complete project architecture, data flow, and technical implementation. 🎯

