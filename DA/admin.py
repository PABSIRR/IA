from django.contrib import admin

# Register your models here.

from DA.models import Info , Entry

admin.site.register(Info)

admin.site.register(Entry)