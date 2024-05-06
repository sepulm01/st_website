#from django.db import models
from django.db import models
#from jsonfield import JSONField
from django.contrib.gis.geos import Point, Polygon
from django.contrib.gis.db import models

# lets us explicitly set upload path and filename
def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

# Create your models here.
class Post(models.Model):
    ''' Modelo para almacenar contenidos de los posteos    '''
    id = models.IntegerField('id', unique=True, primary_key=True)
    title =  models.CharField(max_length=500, null=True)
    tema = models.CharField(max_length=100, null=True)
    contenido=models.TextField('contenido', default='')
    fuente = models.CharField(max_length=900, null=True)
    image_url = models.ImageField(upload_to=upload_to, blank=True, null=True)
    fecha=models.DateTimeField('fecha',null=True)
    icon=models.IntegerField('icon',null=True)
    RRSS_CHOICES = [
    ("LN", "Linkedin"),
    ("X", "X"),
    ("IG", "Instagram"),
    ("FB", "Facebook"),
    ("BG", "Blog"),
    ]
    rrss = models.CharField(max_length=3, choices=RRSS_CHOICES)
    revisar=models.BooleanField('revisar',default=False)
    publicado=models.BooleanField('publicado',default=False)

    def __str__(self):
        return str(self.title)
    
class Fuentes(models.Model):
    tema = models.CharField(max_length=60, null=True)
    texto = models.CharField(max_length=200, null=True)
    titulo = models.CharField(max_length=200, null=True)
    tipos_choices = [
    ("RSS", "rss"),
    ("HTML", "html"),
    ]
    tipo =  models.CharField(max_length=4, choices=tipos_choices)
    url = models.URLField("url")
    estado = models.BooleanField(default=True)

    def __str__(self):
        return str(self.titulo)

class Contenido(models.Model):
    enlace = models.URLField(unique=True, null=True)
    publicado = models.DateField(null=True)
    titulo = models.CharField(max_length=300,null=True)
    fuente = models.ForeignKey('Fuentes', on_delete=models.CASCADE)
    imagen = models.URLField(null=True)

    def __str__(self):
        return str(self.titulo)