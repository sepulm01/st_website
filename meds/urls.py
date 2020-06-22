from django.urls import path
from django.views.generic import TemplateView
from meds.views import paciente_new, contactos, lista_paci, paciente_upd

urlpatterns = [
path('', TemplateView.as_view(template_name="meds/home.html")),
path('paciente/<int:id>/', paciente_upd, name='paciente_upd'), 
path('paciente/', paciente_new, name='paciente_new'), 
path('contactos/<int:id>/', contactos, name='contactos'), 
path('pacientes/', lista_paci, name='lista_paci'), 
]