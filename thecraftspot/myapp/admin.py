from django.contrib import admin
from . models import logintable
# Register your models here.
class showlist(admin.ModelAdmin):
    list_display = ["username","email_id","phone_no"]

admin.site.register(logintable,showlist)