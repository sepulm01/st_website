from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe

# Register your models here.

@admin.register(Contact)
class PostRegist(admin.ModelAdmin):
    list_display = ['email','full_name','status']
    
@admin.register(Estado)
class PostRegist(admin.ModelAdmin):
    list_display = ['estado',]
