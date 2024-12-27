from django.contrib import admin
from .models import User, Student, Tutor, Subject, Certification


# Register your models here.
admin.site.register(User)
admin.site.register(Tutor)
admin.site.register(Student)

admin.site.register(Subject)
admin.site.register(Certification)
