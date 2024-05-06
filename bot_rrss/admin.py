from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe

# Register your models here.

admin.site.site_header = "StreetFlow Services App"
admin.site.index_title = "Menú"
admin.site.site_url = '/'
#admin.site.disable_action('delete_selected')

@admin.register(Post)
class PostRegist(admin.ModelAdmin):
    list_display = ['title','id','tema','publicado','revisar','rrss','fecha']
    #readonly_fields = ('creado',)
# Register your models here.

@admin.register(Fuentes)
class FuentesRegist(admin.ModelAdmin):
    list_display = ['tema','texto','tipo','url','estado']

@admin.register(Contenido)
class ContenidoRegist(admin.ModelAdmin):
    list_display = ['id','titulo','fuente','picture','publicado','enlace',]
    readonly_fields = ('picture',)

    def picture(self, obj):
        if obj.imagen != None:
            return mark_safe('<img src="{url}" height="50" />'.format(url = obj.imagen ))
        else:
            return "NA"
        