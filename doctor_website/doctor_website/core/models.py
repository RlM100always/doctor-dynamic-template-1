from django.db import models


class SiteSettings(models.Model):
    """Doctor's main site configuration"""
    doctor_name = models.CharField(max_length=200, default='ডাঃ সানজিদা ইসলাম চৌধুরী')
    doctor_name_en = models.CharField(max_length=200, default='Dr. Sanjida Islam Chowdhury')
    specialty = models.CharField(max_length=200, default='গাইনী ও প্রসূতি বিশেষজ্ঞ')
    degrees = models.CharField(max_length=300, default='MBBS · FCPS · MRCOG (UK)')
    bio = models.TextField(default='')
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
