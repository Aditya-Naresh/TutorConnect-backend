from django.contrib import admin
from . models import TutorDates, TimeSlots, TuitionRequest
# Register your models here.

admin.site.register(TutorDates)
admin.site.register(TimeSlots)
admin.site.register(TuitionRequest)

