from django.contrib import admin

# Register your models here.

from .models import WikiPage

admin.site.register(WikiPage)