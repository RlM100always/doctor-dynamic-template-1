from django.db import models


class SiteSettings(models.Model):
    """Doctor's main site configuration"""
    doctor_name = models.CharField(max_length=200, default='ডাঃ সানজিদা ইসলাম চৌধুরী')
    doctor_name_en = models.CharField(max_length=200, default='Dr. Sanjida Islam Chowdhury')
    specialty = models.CharField(max_length=200, default='গাইনী ও প্রসূতি বিশেষজ্ঞ')
    degrees = models.CharField(max_length=300, default='MBBS · FCPS · MRCOG (UK)')
    # Replace the old 'bio' with two fields:
    short_bio = models.TextField(verbose_name="সংক্ষিপ্ত পরিচয়", default="")
    detailed_bio = models.TextField(verbose_name="বিস্তারিত পরিচয়", default="")

    phone = models.CharField(max_length=20, default='০১৮১১-২২৩৩৪৪')
    phone_raw = models.CharField(max_length=20, default='+8801811223344')
    whatsapp = models.CharField(max_length=20, default='+8801811223344')
    email = models.EmailField(default='dr.sanjida@example.com')
    facebook_url = models.URLField(blank=True, default='https://facebook.com/dr.sanjida.bd')
    youtube_url = models.URLField(blank=True)
    profile_photo = models.ImageField(upload_to='doctor/', blank=True, null=True)
    profile_photo_url = models.URLField(blank=True, default='https://cdn.sasthyaseba.com/doctors/7410/xoWEh5iyzT9wpngIPNnKbQQiN5AnbUCE8y2hJYpv/dr-sanjida-hossain.jpg')
    years_experience = models.IntegerField(default=22)
    successful_deliveries = models.IntegerField(default=8000)
    google_rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.8)
    google_review_count = models.IntegerField(default=650)
    research_papers = models.IntegerField(default=18)
    booking_fee = models.IntegerField(default=300)
    bkash_number = models.CharField(max_length=20, default='০১৮১১-২২৩৩৪৪')
    nagad_number = models.CharField(max_length=20, default='০১৮১১-২২৩৩৪৪')
    rocket_number = models.CharField(max_length=25, default='০১৮১১২২৩৩৪৪৭')
    map_embed_url = models.TextField(default='', blank=True)
    maps_link = models.URLField(blank=True, default='https://maps.google.com/?q=মিরপুর+ঢাকা')
    meta_title = models.CharField(max_length=200, default='ডাঃ সানজিদা ইসলাম চৌধুরী | গাইনী ও প্রসূতি বিশেষজ্ঞ')
    meta_description = models.TextField(blank=True, default='')

    class Meta:
        verbose_name = 'সাইট সেটিংস'
        verbose_name_plural = 'সাইট সেটিংস'

    def __str__(self):
        return self.doctor_name

    def get_profile_photo(self):
        if self.profile_photo:
            return self.profile_photo.url
        return self.profile_photo_url


class TickerMessage(models.Model):
    message = models.CharField(max_length=300)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'টিকার বার্তা'

    def __str__(self):
        return self.message


class TrustChip(models.Model):
    icon_class = models.CharField(max_length=100, default='fas fa-award')
    text = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text


class HeroDegree(models.Model):
    label = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.label


class AboutHighlight(models.Model):
    icon_class = models.CharField(max_length=100, default='fas fa-graduation-cap')
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=300)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'পরিচিতির হাইলাইট'

    def __str__(self):
        return self.title


class Qualification(models.Model):
    year = models.CharField(max_length=20)
    degree = models.CharField(max_length=200)
    institution = models.CharField(max_length=300)
    icon_class = models.CharField(max_length=100, default='fas fa-graduation-cap')
    TYPE_CHOICES = [
        ('degree', 'স্নাতক ডিগ্রি'),
        ('postgrad', 'পোস্ট-গ্র্যাজুয়েট'),
        ('international', 'আন্তর্জাতিক'),
        ('training', 'বিদেশী প্রশিক্ষণ'),
        ('current', 'বর্তমান পদ'),
    ]
    entry_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='degree')
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'শিক্ষাগত যোগ্যতা'

    def __str__(self):
        return f"{self.year} - {self.degree}"


class Certificate(models.Model):
    number = models.CharField(max_length=10, default='01')
    icon_class = models.CharField(max_length=100, default='fas fa-scroll')
    title = models.CharField(max_length=200)
    description = models.TextField()
    link_text = models.CharField(max_length=100, default='সনদ যাচাই করুন')
    link_url = models.URLField(blank=True)
    is_amber = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'সনদপত্র'

    def __str__(self):
        return self.title


class Chamber(models.Model):
    badge = models.CharField(max_length=100, default='প্রধান চেম্বার')
    name = models.CharField(max_length=200)
    area = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    schedule = models.CharField(max_length=300)
    closed_days = models.CharField(max_length=200, default='শুক্রবার: বন্ধ')
    phone = models.CharField(max_length=30)
    phone_raw = models.CharField(max_length=20, default='+8801811223344')
    icon_class = models.CharField(max_length=100, default='fas fa-hospital-alt')
    is_amber = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'চেম্বার'

    def __str__(self):
        return self.name


class Service(models.Model):
    icon_class = models.CharField(max_length=100, default='fas fa-stethoscope')
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'সেবা'

    def __str__(self):
        return self.title


class FeeItem(models.Model):
    service_name = models.CharField(max_length=200)
    fee = models.IntegerField()
    includes = models.CharField(max_length=300)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'ফি তালিকা'

    def __str__(self):
        return f"{self.service_name} - {self.fee}"


class FeeInfo(models.Model):
    """Extra info shown in fee sidebar"""
    icon_class = models.CharField(max_length=100, default='fas fa-check-circle')
    text = models.CharField(max_length=300)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'ফি তথ্য'

    def __str__(self):
        return self.text


class AppointmentSlot(models.Model):
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'সময় স্লট'

    def __str__(self):
        return self.label


class Review(models.Model):
    reviewer_name = models.CharField(max_length=200)
    avatar_letter = models.CharField(max_length=5, blank=True)
    rating = models.IntegerField(default=5)
    review_text = models.TextField()
    is_verified = models.BooleanField(default=True)
    is_accent = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'রিভিউ'

    def __str__(self):
        return f"{self.reviewer_name} - {self.rating}★"

    def save(self, *args, **kwargs):
        if not self.avatar_letter:
            self.avatar_letter = self.reviewer_name[0] if self.reviewer_name else 'র'
        super().save(*args, **kwargs)

    def get_stars(self):
        return '★' * self.rating + '☆' * (5 - self.rating)


class RatingBar(models.Model):
    stars = models.IntegerField()
    percentage = models.IntegerField()

    class Meta:
        ordering = ['-stars']

    def __str__(self):
        return f"{self.stars}★ - {self.percentage}%"

class Video(models.Model):
    youtube_url = models.CharField(max_length=300)
    title = models.CharField(max_length=200)
    tag = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'ভিডিও'

    def __str__(self):
        return self.title

    def get_embed_url(self):
        url = self.youtube_url.strip()
        # Handle existing embed links
        if 'youtube.com/embed/' in url:
            return url
        
        # Handle short links (youtu.be/ID)
        elif 'youtu.be/' in url:
            # split by / then split by ? to remove parameters
            vid_id = url.split('youtu.be/')[1].split('?')[0].split('&')[0]
            return f"https://www.youtube.com/embed/{vid_id}"
        
        # Handle standard links (youtube.com/watch?v=ID)
        elif 'v=' in url:
            vid_id = url.split('v=')[1].split('&')[0]
            return f"https://www.youtube.com/embed/{vid_id}"
            
        return url


class BlogPost(models.Model):
    icon_class = models.CharField(max_length=100, default='fas fa-baby')
    category = models.CharField(max_length=100)
    title = models.CharField(max_length=300)
    excerpt = models.TextField()
    full_content = models.TextField(blank=True)
    is_large = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'ব্লগ পোস্ট'

    def __str__(self):
        return self.title


class MediaCoverage(models.Model):
    icon_class = models.CharField(max_length=100, default='fas fa-newspaper')
    outlet_name = models.CharField(max_length=200)
    description = models.CharField(max_length=300)
    is_amber = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'মিডিয়া কভারেজ'

    def __str__(self):
        return self.outlet_name


class TeamMember(models.Model):
    role = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    qualifications = models.CharField(max_length=300)
    photo = models.ImageField(upload_to='team/', blank=True, null=True)
    photo_url = models.URLField(blank=True)
    icon_class = models.CharField(max_length=100, default='fas fa-user-md')
    is_lead = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'টিম সদস্য'

    def __str__(self):
        return self.name

    def get_photo(self):
        if self.photo:
            return self.photo.url
        return self.photo_url


class FAQ(models.Model):
    question = models.CharField(max_length=400)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'FAQ'

    def __str__(self):
        return self.question


class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'যোগাযোগ বার্তা'

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%d/%m/%Y')}"




class GalleryItem(models.Model):
    """Single image in doctor's gallery"""
    title = models.CharField(max_length=200, blank=True, help_text="ছবির শিরোনাম (ঐচ্ছিক)")
    image = models.ImageField(upload_to='gallery/', blank=True, null=True, help_text="আপলোড করুন ছবি")
    image_url = models.URLField(blank=True, help_text="অথবা বাহ্যিক ছবির লিংক দিন")
    order = models.IntegerField(default=0, help_text="ক্রম")
    is_active = models.BooleanField(default=True, help_text="সক্রিয়")

    class Meta:
        ordering = ['order']
        verbose_name = 'গ্যালারির ছবি'
        verbose_name_plural = 'গ্যালারির ছবি'

    def __str__(self):
        return self.title or f"ছবি #{self.id}"

    def get_image_url(self):
        """Return image URL from upload or external link"""
        if self.image:
            return self.image.url
        return self.image_url or ''
    
    
    
    
    """
=============================================================================
OFFLINE CHAMBER MANAGEMENT SYSTEM — MODELS
=============================================================================
Add these models to:  core/models.py  (append at the bottom)
=============================================================================
"""

from django.db import models
from django.utils import timezone


# ─── DISTRICT / AREA CHOICES (Bangladesh) ────────────────────────────────────
DISTRICT_CHOICES = [
    ('tangail', 'টাঙ্গাইল'),
    ('dhaka', 'ঢাকা'),
    ('gazipur', 'গাজীপুর'),
    ('narayanganj', 'নারায়ণগঞ্জ'),
    ('manikganj', 'মানিকগঞ্জ'),
    ('munshiganj', 'মুন্সিগঞ্জ'),
    ('narsingdi', 'নরসিংদী'),
    ('mymensingh', 'ময়মনসিংহ'),
    ('jamalpur', 'জামালপুর'),
    ('kishorganj', 'কিশোরগঞ্জ'),
    ('other', 'অন্যান্য'),
]

GENDER_CHOICES = [
    ('male', 'পুরুষ'),
    ('female', 'মহিলা'),
    ('other', 'অন্যান্য'),
]

VISIT_TYPE_CHOICES = [
    ('new', 'নতুন রোগী'),
    ('followup', 'ফলো-আপ'),
]

PAYMENT_METHOD_CHOICES = [
    ('cash', 'নগদ'),
    ('bkash', 'বিকাশ'),
    ('nagad', 'নগদ (মোবাইল)'),
    ('card', 'কার্ড'),
]

PAYMENT_STATUS_CHOICES = [
    ('paid', 'পরিশোধিত'),
    ('due', 'বাকি'),
    ('partial', 'আংশিক'),
]


# ─── CHAMBER PATIENT ─────────────────────────────────────────────────────────
class ChamberPatient(models.Model):
    """Master record for each unique patient"""
    patient_id      = models.CharField(max_length=20, unique=True, editable=False)
    name            = models.CharField(max_length=200, verbose_name='রোগীর নাম')
    phone           = models.CharField(max_length=20, unique=True, verbose_name='মোবাইল নম্বর')
    age             = models.PositiveIntegerField(verbose_name='বয়স', null=True, blank=True)
    gender          = models.CharField(max_length=10, choices=GENDER_CHOICES, default='female', verbose_name='লিঙ্গ')
    district        = models.CharField(max_length=30, choices=DISTRICT_CHOICES, default='tangail', verbose_name='জেলা')
    area            = models.CharField(max_length=200, verbose_name='এলাকা', blank=True)
    address         = models.TextField(verbose_name='ঠিকানা', blank=True)
    first_visit_date = models.DateField(default=timezone.now, verbose_name='প্রথম ভিজিটের তারিখ')
    notes           = models.TextField(blank=True, verbose_name='নোট')
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'চেম্বার রোগী'
        verbose_name_plural = 'চেম্বার রোগী'

    def __str__(self):
        return f"{self.patient_id} — {self.name} ({self.phone})"

    def save(self, *args, **kwargs):
        if not self.patient_id:
            # Auto-generate: CP-2025-0001
            year = timezone.now().year
            last = ChamberPatient.objects.filter(
                patient_id__startswith=f'CP-{year}-'
            ).order_by('patient_id').last()
            if last:
                num = int(last.patient_id.split('-')[-1]) + 1
            else:
                num = 1
            self.patient_id = f'CP-{year}-{num:04d}'
        super().save(*args, **kwargs)

    def get_total_visits(self):
        return self.visits.count()

    def get_last_visit(self):
        return self.visits.order_by('-visit_date').first()

    def get_total_paid(self):
        total = sum(p.total_amount for p in
                    ChamberPayment.objects.filter(visit__patient=self, payment_status='paid'))
        return total


# ─── CHAMBER VISIT ────────────────────────────────────────────────────────────
class ChamberVisit(models.Model):
    """Each visit by a patient"""
    patient         = models.ForeignKey(ChamberPatient, on_delete=models.CASCADE,
                                        related_name='visits', verbose_name='রোগী')
    visit_date      = models.DateField(default=timezone.now, verbose_name='ভিজিটের তারিখ')
    visit_type      = models.CharField(max_length=10, choices=VISIT_TYPE_CHOICES,
                                       default='new', verbose_name='ভিজিটের ধরন')
    symptoms        = models.TextField(blank=True, verbose_name='লক্ষণ')
    diagnosis       = models.TextField(blank=True, verbose_name='রোগ নির্ণয়')
    followup_date   = models.DateField(null=True, blank=True, verbose_name='পরবর্তী ফলো-আপ তারিখ')
    doctor_fee      = models.DecimalField(max_digits=8, decimal_places=2, default=0,
                                          verbose_name='ডাক্তার ফি')
    notes           = models.TextField(blank=True, verbose_name='নোট')
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-visit_date', '-created_at']
        verbose_name = 'ভিজিট'
        verbose_name_plural = 'ভিজিটসমূহ'

    def __str__(self):
        return f"{self.patient.name} — {self.visit_date} ({self.get_visit_type_display()})"

    def get_payment(self):
        return ChamberPayment.objects.filter(visit=self).first()


# ─── CHAMBER PAYMENT ─────────────────────────────────────────────────────────
class ChamberPayment(models.Model):
    """Payment record linked to a visit"""
    visit               = models.OneToOneField(ChamberVisit, on_delete=models.CASCADE,
                                               related_name='payment', verbose_name='ভিজিট')
    consultation_fee    = models.DecimalField(max_digits=8, decimal_places=2, default=0,
                                              verbose_name='পরামর্শ ফি')
    additional_charge   = models.DecimalField(max_digits=8, decimal_places=2, default=0,
                                              verbose_name='অতিরিক্ত চার্জ', blank=True)
    total_amount        = models.DecimalField(max_digits=8, decimal_places=2, default=0,
                                              verbose_name='মোট পরিমাণ')
    payment_method      = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES,
                                           default='cash', verbose_name='পেমেন্ট পদ্ধতি')
    payment_status      = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES,
                                           default='paid', verbose_name='পেমেন্ট অবস্থা')
    created_at          = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'পেমেন্ট'
        verbose_name_plural = 'পেমেন্টসমূহ'

    def __str__(self):
        return f"{self.visit.patient.name} — ৳{self.total_amount} ({self.get_payment_status_display()})"

    def save(self, *args, **kwargs):
        self.total_amount = (self.consultation_fee or 0) + (self.additional_charge or 0)
        super().save(*args, **kwargs)