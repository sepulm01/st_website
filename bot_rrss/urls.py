from django.contrib import admin
from django.urls import path, include
from bot_rrss import views
from rest_framework import routers

from rest_framework.documentation import include_docs_urls

router = routers.DefaultRouter()
router.register(r'noticias', views.NoticiasView, 'noticias')

urlpatterns = [
    path('feed/', views.post_feed_endpoint_view, name='post_feed'),
    path('feed/hoy', views.get_noticias_hoy, name='hoy_feed'),
    path('feed/all', views.get_noticias_all, name='todas-noticias'),
    path('api/v1/', include(router.urls)),
    path('docs', include_docs_urls(title="Docs Noticias API"))
    
]