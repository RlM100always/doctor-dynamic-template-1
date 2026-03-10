from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Usage: {{ status_counts|get_item:val }}"""
    return dictionary.get(key, 0)


"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2.  models.py  —  Add these properties to Appointment model
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

# Add inside your Appointment model class:

from django.utils import timezone

@property
def is_today(self):
    return self.date == timezone.now().date()

@property
def is_upcoming(self):
    return self.date > timezone.now().date()

@property
def is_past(self):
    return self.date < timezone.now().date()


"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3.  templates/admin_panel/base_admin.html
    — load the tag at top of base template (once)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {% load app_tags %}


4.  URLs  —  make sure these two routes exist
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
