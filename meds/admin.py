from django.contrib import admin
from meds.models import *
# Register your models here.


class PrevInline(admin.TabularInline):
    model = Prevision
    #form = EnvioForm
    extra = 0
    list_display = ['nom_prev']

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ['nombre','apellido','rut','edad','sexo']
    #inlines = [PrevInline, ]

admin.site.register(Pais)

admin.site.register(Region)

admin.site.register(Prov)

admin.site.register(Comuna)

admin.site.register(Contacto)