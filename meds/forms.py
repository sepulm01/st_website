from django.forms import ModelForm, TextInput, Select
from . import models
from django.forms.models import inlineformset_factory

class Paciente_f(ModelForm):
    class Meta:
        model = models.Paciente
        fields = '__all__'

        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control'}),
            'apellido': TextInput(attrs={'class': 'form-control'}),
            'rut': TextInput(attrs={'class': 'form-control'}),
            'edad': TextInput(attrs={'class': 'form-control'}),
            'sexo': TextInput(attrs={'class': 'form-control'}),
            'calle': TextInput(attrs={'class': 'form-control'}),
            'pais': Select(attrs={'class': 'form-control'}),
            'region': Select(attrs={'class': 'form-control'}),
            'comuna': Select(attrs={'class': 'form-control'}),
            'fono': TextInput(attrs={'class': 'form-control'}),
            'sange': TextInput(attrs={'class': 'form-control'}),
        }


class CollectionContactoForm(ModelForm):

    class Meta:
        model = models.Contacto
        exclude = ()

CollectionContacto = inlineformset_factory(
    models.Paciente,models.Contacto,  form=CollectionContactoForm,
    fields=['nombre', 'fono', 'parentesco'], extra=0, can_delete=True
    )