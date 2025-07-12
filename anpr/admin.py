from django.contrib import admin

# Register your models here.
from django.contrib import admin
from . models import Residents,Logbook



admin.site.register(Residents)
admin.site.register(Logbook)