# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls import include, url, handler404, handler500
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve

from django.urls import path
from django.views.generic import TemplateView
from robot.views import new_descriptor, chat_bot
from django.utils.functional import curry
from django.views.defaults import *

admin.autodiscover()


handler500 = curry(server_error, template_name='500.html')
handler404 = curry(page_not_found, template_name='404.html')
handler403 = curry(permission_denied, template_name='403.html')

urlpatterns = [
    url(r'^sitemap\.xml$', sitemap,
        {'sitemaps': {'cmspages': CMSSitemap}}),
    url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
    path('mapa/', TemplateView.as_view(template_name="mapa.html")),
    path('index/', TemplateView.as_view(template_name="index.html")),
    path('index2/', TemplateView.as_view(template_name="index2.html")),
    path('robot/', TemplateView.as_view(template_name="robot.html")),
    path('ajax/descriptores/', new_descriptor, name='new_descriptor'), 
    path('ajax/chat/', chat_bot, name='chat_bot'),
    path('meds/', include('meds.urls')),
]

urlpatterns += i18n_patterns(
    url(r'^admin/', admin.site.urls),  # NOQA
    url(r'^', include('cms.urls')),

)

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns = [
        url(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        ] + staticfiles_urlpatterns() + urlpatterns
