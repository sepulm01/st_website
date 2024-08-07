# Create your tasks here
from __future__ import absolute_import, unicode_literals
#import requests
from celery import shared_task
from datetime import datetime, timedelta
from .models import *
from .revisa_email import *
from django.contrib.gis.geos import Point, Polygon


@shared_task
def ia_email():
    procec = procesa()
    return procec


