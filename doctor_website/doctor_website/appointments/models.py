from django.db import models


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'অপেক্ষমাণ'),
        ('confirmed', 'নিশ্চিত'),
        ('cancelled', 'বাতিল'),
        ('completed', 'সম্পন্ন'),
    ]
    patient_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    date = models.DateField()
    time_slot = models.CharField(max_length=100)
    note = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    chamber = models.CharField(max_length=200, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_note = models.TextField(blank=True, help_text='ডাক্তারের নোট (রোগী দেখবে না)')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'অ্যাপয়েন্টমেন্ট'

    def __str__(self):
        return f"{self.patient_name} - {self.date} {self.time_slot}"

    def get_status_badge_class(self):
        classes = {
            'pending': 'badge-warning',
            'confirmed': 'badge-success',
            'cancelled': 'badge-danger',
            'completed': 'badge-info',
        }
        return classes.get(self.status, 'badge-secondary')
