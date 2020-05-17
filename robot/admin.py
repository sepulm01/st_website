from django.contrib import admin
from .models import Descriptor, Persona

# Register your models here.


admin.site.register(Descriptor)


class DescInline(admin.TabularInline):
    model = Descriptor
    #form = EnvioForm
    extra = 0
    list_display = ['did','persona','user_foto', 'np_field']

#admin.site.register(Persona)
@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ['pid','nombre','edad','sexo']
    inlines = [DescInline, ]