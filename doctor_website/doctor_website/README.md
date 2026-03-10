# ডাক্তার ওয়েবসাইট — Django Dynamic Website
## Dr. Sanjida Islam Chowdhury — Gynaecology & Obstetrics Specialist

---

## 📁 Project Structure

```
doctor_website/
│
├── config/                     ← Django project config
│   ├── __init__.py
│   ├── settings.py             ← All settings (DB, Static, Media, etc.)
│   ├── urls.py                 ← Root URL configuration
│   └── wsgi.py
│
├── core/                       ← Main app (public site + admin panel)
│   ├── management/
│   │   └── commands/
│   │       └── seed_data.py    ← Seeds initial data from original site
│   ├── migrations/             ← Auto-generated after makemigrations
│   ├── admin.py
│   ├── admin_urls.py           ← Admin panel URL routes
│   ├── admin_views.py          ← All admin panel views
│   ├── context_processors.py   ← Injects `site` into every template
│   ├── models.py               ← ALL dynamic content models
│   ├── urls.py                 ← Public site routes
│   └── views.py                ← Public views (home, blog, contact)
│
├── appointments/               ← Appointment booking app
│   ├── migrations/
│   ├── admin.py
│   ├── models.py               ← Appointment model
│   ├── urls.py
│   └── views.py                ← AJAX booking endpoint
│
├── templates/
│   ├── base.html               ← Public site base layout
│   ├── core/
│   │   └── home.html           ← Main dynamic homepage (all sections)
│   └── admin_panel/
│       ├── base_admin.html     ← Admin sidebar + topbar layout
│       ├── login.html
│       ├── dashboard.html      ← Stats, recent appointments & messages
│       ├── site_settings.html  ← Doctor profile, contact, payment, SEO
│       ├── tickers.html
│       ├── qualifications.html
│       ├── certificates.html
│       ├── chambers.html
│       ├── services.html
│       ├── fees.html
│       ├── appointments.html   ← Full CRUD + status management
│       ├── reviews.html
│       ├── videos.html
│       ├── blogs.html
│       ├── team.html
│       ├── faqs.html
│       ├── messages.html
│       └── media.html
│
├── static/
│   ├── css/
│   │   └── style.css           ← Original site CSS (unchanged)
│   └── js/
│       └── main.js             ← Original site JS (unchanged)
│
├── media/                      ← Uploaded images (doctor photos, team, etc.)
│
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run

### Step 1 — Install Python & pip
Make sure Python 3.10+ is installed.

### Step 2 — Install dependencies
```bash
cd doctor_website
pip install -r requirements.txt
```

### Step 3 — Run database migrations
```bash
python manage.py makemigrations core appointments
python manage.py migrate
```

### Step 4 — Seed the database with original site data
```bash
python manage.py seed_data
```
This command:
- Creates all initial content (tickers, services, fees, faqs, team, etc.)
- Creates superuser: **admin** / **admin123**

### Step 5 — Collect static files (optional, for production)
```bash
python manage.py collectstatic
```

### Step 6 — Run the development server
```bash
python manage.py runserver
```

---

## 🌐 URLs

| URL | Description |
|-----|-------------|
| `http://127.0.0.1:8000/` | Public website homepage |
| `http://127.0.0.1:8000/admin-panel/` | Doctor's admin panel |
| `http://127.0.0.1:8000/admin-panel/login/` | Admin login |
| `http://127.0.0.1:8000/django-admin/` | Django built-in admin |

**Default Admin Credentials:**
- Username: `admin`
- Password: `admin123`

---

## 🔐 Admin Panel Features

The doctor has **full control** over every section of the website:

| Admin Page | What Doctor Can Manage |
|-----------|------------------------|
| **Dashboard** | Overview stats, recent appointments, unread messages |
| **Site Settings** | Name, photo, bio, phone, email, WhatsApp, bKash/Nagad/Rocket numbers, Google Map, SEO meta tags |
| **Ticker Messages** | News ticker bar at the top of the site |
| **Qualifications** | Education timeline (MBBS, FCPS, MRCOG, etc.) |
| **Certificates** | Certificates & affiliations section |
| **Chambers** | Chamber locations, address, schedule, phone |
| **Services** | Medical services offered |
| **Fee Chart** | Consultation fees, featured packages |
| **Appointments** | View, confirm, cancel, complete bookings + add notes |
| **Reviews** | Add/edit patient reviews, toggle visibility |
| **Videos** | YouTube video gallery |
| **Blog Posts** | Write/edit health articles with full HTML content |
| **Team Members** | Staff profiles with photo upload |
| **FAQs** | Questions & answers section |
| **Contact Messages** | View patient inquiries, mark as read/delete |
| **Media Coverage** | Press mentions & awards |

---

## 🗄️ Database Models

### `SiteSettings`
Single-row config: doctor name, photo, bio, phone, social links, payment numbers, stats, SEO.

### `Appointment`
Patient bookings with status: `pending → confirmed → completed / cancelled`

### `ContactMessage`
Messages from the contact form, with read/unread tracking.

### All other models
`TickerMessage`, `TrustChip`, `HeroDegree`, `AboutHighlight`, `Qualification`,
`Certificate`, `Chamber`, `Service`, `FeeItem`, `AppointmentSlot`,
`Review`, `RatingBar`, `Video`, `BlogPost`, `MediaCoverage`, `TeamMember`, `FAQ`

---

## ⚙️ Tech Stack

- **Backend:** Django 4.2 (Python)
- **Database:** SQLite (dev) — easily switchable to PostgreSQL/MySQL
- **Frontend:** Original HTML/CSS/JS (unchanged visual design)
- **Image uploads:** Django + Pillow
- **Authentication:** Django's built-in auth system

---

## 🔧 Production Checklist

1. Set `DEBUG = False` in `settings.py`
2. Change `SECRET_KEY` to a strong random value
3. Set `ALLOWED_HOSTS` to your domain
4. Use PostgreSQL instead of SQLite
5. Serve static & media files via nginx/Apache
6. Use gunicorn as WSGI server
