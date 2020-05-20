from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse
from robot.models import Persona, Descriptor
import numpy as np
import pickle
import base64
import face_recognition

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

# Create a new chat bot named Charlie
chatbot = ChatBot('Charlie')

trainer = ChatterBotCorpusTrainer(chatbot)

trainer.train(
    "chatterbot.corpus.spanish.greetings",
    #"chatterbot.corpus.spanish.IA"
)

# Create your views here.
def new_descriptor(request):
    '''rutina AJAX para almacenar el descriptor.'''
    TOLERANCE = 0.6

    desc = { }

    def busca(descrip,rec=0):
        descrip = np.fromstring(descrip, dtype=float, sep=',')
        personas = Persona.objects.all()
        persona = ""
        conocidos = []
        for persona in personas:
            results = []
            caras = Descriptor.objects.filter(persona=persona)
            for e in caras:
                np_bytes = base64.b64decode(e.np_field)
                if len(np_bytes) != 0:
                    np_array = pickle.loads(np_bytes)
                    #print('cara',e,'np_array:',type(np_array),'\ndescrip:',type(descrip))
                    results.append(face_recognition.compare_faces([np_array], descrip, TOLERANCE)[0])
            #print(results, type(persona),persona)
            if True in results:
                print("Reconoció a",persona)
                conocidos.append(True)
                if rec != 0: 
                    np_bytes = pickle.dumps(descrip)
                    np_base64 = base64.b64encode(np_bytes)
                    b= Descriptor(persona=persona, np_field = np_base64)
                    b.save()
                    print("y creo descriptor")
                break
            else:
                conocidos.append(False)
        
        return conocidos, persona

    if request.method == 'POST':
        nombre = request.POST['nombre']
        descrip = request.POST['descriptores'] 
        record = request.POST['record'] 
        sexo = request.POST['sexo']
        anos = float(request.POST['anos'])
        anos = int(anos)
        conocidos, _ = busca(descrip,rec=1)
        print('conocidos:',conocidos)
        if True in conocidos or conocidos==[]:
            estado = 'Ya te conocía :)'
            pass
        else:
            p=Persona(sexo=sexo,edad=anos)
            print("crear nueva persona", sexo, anos)
            p.save()
            np_bytes = pickle.dumps(np.fromstring(descrip, dtype=float, sep=','))
            np_base64 = base64.b64encode(np_bytes)
            b= Descriptor(persona=p, np_field = np_base64)
            print("crear nuevo descriptor")
            b.save()
            estado = 'Creado como nueva persona'
        desc = { 'status': estado }
    else:
        descrip = request.GET['descriptores']
        sexo = request.GET['sexo'] 
        anos = float(request.GET['anos'])
        anos = int(anos)
        nombre = "name"
        conocidos, persona = busca(descrip,rec=0)
        #print(conocidos,type(persona.nombre),persona.edad, persona.sexo)
        if any(conocidos):
            desc = {
                'nombre':persona.nombre,
                'sexo': persona.sexo,
                'edad': persona.edad
            }

    return JsonResponse(desc)

def get_descriptor(pid):
    desc = Descriptor.objects.filter(pid=pid)
    np_bytes = base64.b64decode(desc.np_field)
    np_array = pickle.loads(np_bytes)
    return np_array

def chat_bot(request):
    if request.method == 'GET':
        mensaje = request.GET['mensaje']
        resp = chatbot.get_response(mensaje)
        print("in:",mensaje,"\nout:",resp, type(resp))
        #resp = 'Comunicación exitosa!' + mensaje
        desc = {
                'respuesta':str(resp),
                }

    return JsonResponse(desc)