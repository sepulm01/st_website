from django.db import models

# Create your models here.

class Paciente(models.Model):
  SEX = [
    ('h','Hombre'),
    ('m','Mujer'),
    ]
  
  TIPO = [
    ('O-','O-'),
    ('O+','O+'),
    ('A-','A-'),
    ('A+','A+'),
    ('B-','B-'),
    ('B+','B+'),
    ('AB-','AB-'),
    ('AB+','AB+'),
     ]

  pid = models.AutoField(primary_key=True)
  nombre = models.CharField("Nombre",max_length=20)
  apellido = models.CharField("Apellido",max_length=20)
  rut = models.CharField("Rut",max_length=20)
  edad = models.IntegerField("Edad", default=0)
  sexo = models.CharField("Sexo",choices=SEX ,max_length=8)
  calle = models.CharField("Calle",max_length=40)
  comuna = models.CharField("Comuna",max_length=20)
  region = models.CharField("Región",max_length=20)
  fono = models.CharField("Región",max_length=12)
  sange = models.CharField("sange",choices=TIPO ,max_length=10)
  
  class Meta:
      verbose_name_plural = "Pacientes"

  def __str__(self):
      return str(self.nombre)

class Patologias(models.Model):
    nombre = models.CharField("Nombre",max_length=50)

class Prevision(models.Model):
    nom_prev =  models.CharField("Prevision",max_length=30)

class Alergias(models.Model):
    nom_aler = models.CharField("Alergia",max_length=30)

class Contacto(models.Model):
    nombre = models.CharField("Nombre",max_length=20)
    fono = models.CharField("Región",max_length=12)
    parentesco = models.CharField("Nombre",max_length=20)

class Medicamentos(models.Model):
    med_nom = models.CharField("Nombre",max_length=20)
    dosis = models.CharField("Nombre",max_length=20)