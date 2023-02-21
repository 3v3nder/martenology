from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Client)
admin.site.register(Treatment)
admin.site.register(Sales)
admin.site.register(Appointment)
admin.site.register(Doctor)
admin.site.register(Report)
admin.site.register(Subscriptions)
