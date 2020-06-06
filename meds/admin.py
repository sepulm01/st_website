from django.contrib import admin
from meds.models import Paciente, Patologias, Prevision, Alergias
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