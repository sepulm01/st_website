from .models import Persona, Descriptor
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
import face_recognition
import os
import numpy as np
import pickle
import base64


@receiver(post_save, sender=Descriptor)
def descriptor_agregar(sender, instance, created, **kwargs):
	''' pasa la foto a descriptor (numpy ) y este se guarda como bytes en el modelo'''
	print("instance.did", instance.did)


