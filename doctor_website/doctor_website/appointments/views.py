from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Appointment
from core.models import AppointmentSlot


@require_POST
def book_appointment(request):
    try:
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        date = data.get('date', '').strip()
        time_slot = data.get('time_slot', '').strip()
        note = data.get('note', '').strip()

        if not name or not phone or not date or not time_slot:
            return JsonResponse({'success': False, 'error': 'সব প্রয়োজনীয় তথ্য দিন।'})

        appt = Appointment.objects.create(
            patient_name=name,
            phone=phone,
            date=date,
            time_slot=time_slot,
            note=note,
        )
        return JsonResponse({'success': True, 'id': appt.pk})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
