from django.urls import path
from django.views.generic import TemplateView
from meds.views import comunas

urlpatterns = [
#path('', TemplateView.as_view(template_name="meds/meds.html")),
path('', comunas, name='comunas'), 
]