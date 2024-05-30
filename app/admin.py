from django.contrib import admin
from .models import Teacher, Question, User, Admin

# Register your models here.
admin.site.register(Teacher)
admin.site.register(Question)
admin.site.register(User)
admin.site.register(Admin)
