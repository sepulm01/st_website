from django.db import models


# Create your models here.

def my_awesome_upload_function(instance, filename):
    return 'Foto_perfiles_{0}/{1}'.format(instance.persona, filename)

class Persona(models.Model):
    pid = models.AutoField(primary_key=True)
    nombre = models.CharField("Nombre",max_length=20)
    edad = models.IntegerField("Edad", default=0)
    sexo = models.CharField("Sexo",max_length=8)
    
    class Meta:
        verbose_name_plural = "Personas"

    def __str__(self):
        return str(self.nombre)

class Descriptor(models.Model):
    did = models.AutoField(primary_key=True)
    persona =models.ForeignKey('Persona', on_delete=models.PROTECT)
    user_foto = models.ImageField(upload_to=my_awesome_upload_function, null=True,blank=True,)
    np_field = models.BinaryField()

class Compras(models.Model):
    cid = models.AutoField(primary_key=True)
    persona =models.ForeignKey('Persona', on_delete=models.CASCADE)
    producto = models.CharField("Producto",max_length=20)
    cant = models.IntegerField("Cantidad", default=1)
    Fecha = models.DateTimeField('Fecha',auto_now_add=True)