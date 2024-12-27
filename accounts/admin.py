from django.contrib import admin
<<<<<<< HEAD
from .models import User, Student, Tutor, Subject, Certification
=======
from . models import User, Student, Tutor

>>>>>>> a85a3b13 (User Registration endpoint completed)


# Register your models here.
admin.site.register(User)
admin.site.register(Tutor)
admin.site.register(Student)

admin.site.register(Subject)
admin.site.register(Certification)
