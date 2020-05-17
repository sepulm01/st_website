from .models import Persona, Descriptor
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
import face_recognition
import os
import numpy as np
import pickle
import base64

def face_desc():
    ''' coloca el descriptor a todas los registros de descriptor'''
    objects = Descriptor.objects.all()
    for e in objects:
        if e.user_foto != None:
            print(e.user_foto.path)
            known_image = face_recognition.load_image_file(e.user_foto.path)
            pre_pro = face_recognition.face_encodings(known_image)
            if type(pre_pro) != list:
                encoding = face_recognition.face_encodings(known_image)[0]
                print("pasa encoding")
                np_bytes = pickle.dumps(encoding)
                np_base64 = base64.b64encode(np_bytes)
                e.np_field = np_base64
                print("pasa e.np_field = np_base64")
                print(type(e),dir(e), e.np_field)
                e.save()
                print("salvó y fin")