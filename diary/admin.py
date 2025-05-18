from django.contrib import admin

# Register your models here.
from .models import Writing

class WritingAdmin(admin.ModelAdmin):
    search_fields=['subject']

admin.site.register(Writing, WritingAdmin)
