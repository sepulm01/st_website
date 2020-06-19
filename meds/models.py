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
  pais = models.ForeignKey('Pais',on_delete=models.PROTECT)
  region = models.ForeignKey('Region',on_delete=models.PROTECT)
  comuna = models.ForeignKey('Comuna',on_delete=models.PROTECT)
  fono = models.CharField("Fono",max_length=12)
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
    paciente = models.ForeignKey('Paciente',on_delete=models.PROTECT)

class Medicamentos(models.Model):
    med_nom = models.CharField("Nombre",max_length=20)
    dosis = models.CharField("Nombre",max_length=20)



class Pais(models.Model):
  pais_id = models.IntegerField("Código País",blank=True)
  pais_name = models.CharField("Nombre País",max_length=20)

  def __str__(self):
    return str(self.pais_name)

  class Meta:
    verbose_name_plural = "Paises"

class Region(models.Model):
  reg_id = models.IntegerField("Código Región", default=0)
  reg_name = models.CharField("Nombre Región",max_length=20)
  reg_pais = models.ForeignKey('Pais',on_delete=models.PROTECT)

  def __str__(self):
    return str(self.reg_name)

  class Meta:
    verbose_name_plural = "Regiones"

class Prov(models.Model):
  prov_id = models.IntegerField("Código Provincia", default=0)
  prov_name = models.CharField("Nombre Provincia",max_length=20)
  prov_reg = models.ForeignKey('Region',on_delete=models.PROTECT)

  def __str__(self):
    return str(self.prov_name)

  class Meta:
    verbose_name_plural = "Provincias"

class Comuna(models.Model):
  com_id = models.IntegerField("Código Comuna", default=0)
  com_name = models.CharField("Nombre Comuna",max_length=20)
  prov_reg = models.ForeignKey('Prov',on_delete=models.PROTECT)

  def __str__(self):
    return str(self.com_name)

  class Meta:
    verbose_name_plural = "Comunas"