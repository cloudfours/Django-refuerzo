from django.contrib import admin

from app.models import Choices, Question

# Register your models here.
admin.site.register(Choices)
admin.site.register(Question)