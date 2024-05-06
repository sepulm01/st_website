# Create your tasks here
from __future__ import absolute_import, unicode_literals
#import requests
from celery import shared_task
from datetime import datetime, timedelta
import pytz
from .models import Post
from .linkedin_main import hace_publicacion_cola
from .instagram_main import hace_publicacion_ig
from django.contrib.gis.geos import Point, Polygon
from .proceso_fuentes import proceso_diario, revisa_multimedia

@shared_task
def publica_linkedin():
    procec = hace_publicacion_cola()
    return procec

@shared_task
def publica_instagram():
    procec = hace_publicacion_ig()
    return procec

@shared_task
def get_fuentes():
    proceso_diario() #Actualiza la base de datos con contenidos del día de hoy
    revisa_multimedia() # Levanta las imagenes y actualiza los contenidos con foto si es que existe

