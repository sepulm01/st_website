from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse
from robot.models import Persona, Descriptor, Compras
import numpy as np
import pickle
import base64
import face_recognition

#from chatterbot import ChatBot
#from chatterbot.trainers import ListTrainer
#from chatterbot.trainers import ChatterBotCorpusTrainer

import re
import pytz
from django.db.models.functions import Trunc

SCL = pytz.timezone('America/Santiago')
# Create a new chat bot named Charlie
#chatbot = ChatBot('Exact Response Example Bot', 
    # logic_adapters=[
    #     {
    #         'import_path': 'chatterbot.logic.BestMatch'
    #     },
    #     {
    #         'import_path': 'chatterbot.logic.SpecificResponseAdapter',
    #         'input_text': 'ayuda',
    #         'output_text': 'Ok, here is a link: http://chatterbot.rtfd.org'
    #     }
    # ]
    # )
# trainer = ChatterBotCorpusTrainer(chatbot)
# trainer.train(
#     "chatterbot.corpus.spanish.greetings",
#     #"chatterbot.corpus.spanish.IA"
# )

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
        #print(request, request.POST['nombre'])
        nombre = request.POST['nombre']
        descrip = request.POST['descriptores'] 
        record = request.POST['record'] 
        sexo = request.POST['sexo']
        anos = float(request.POST['anos'])
        anos = int(anos)
        prod = request.POST['produc']
        conocidos, p = busca(descrip,rec=1)
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
        if prod != None:
            c = Compras(persona=p,producto=prod)
            c.save()
    else:
        descrip = request.GET['descriptores']
        sexo = request.GET['sexo'] 
        anos = float(request.GET['anos'])
        anos = int(anos)
        nombre = "name"
        compra = "sin compras"
        conocidos, persona = busca(descrip,rec=0)
        print(persona)
        compra = Compras.objects.filter(persona=persona).order_by('Fecha')
        if len(compra) > 0:
            print(len(compra), type(compra))
            compra = list(compra.values('producto','cant',fecha=Trunc('Fecha', 'second', tzinfo=SCL)))[-1]
            print(type(compra))
        #print(conocidos,type(persona.nombre),persona.edad, persona.sexo)
        if any(conocidos):
            desc = {
                'nombre':persona.nombre,
                'sexo': persona.sexo,
                'edad': persona.edad,
                'compra': compra
            }

    return JsonResponse(desc)

def get_descriptor(pid):
    desc = Descriptor.objects.filter(pid=pid)
    np_bytes = base64.b64decode(desc.np_field)
    np_array = pickle.loads(np_bytes)
    return np_array

def chat_bot(request):
    list_syn  = {
    'cocacola': {'coke', 'coca', 'cocacola', 'cola'},
    'zero': {'zero', 'diet', 'cero', 'la negra', 'light', 'liviana', 'dietética','0','00', 'acero'},
    'original':{'original','normal'},
    'pepsi': {'pepsi'},
    '7up': {'7up', 'seven', 'up'},
    'kem':{'kem','quién', 'kim', 'quien'},
    'piña':{'piña'},
    'xtream':{'stream', 'energética', 'estetica', 'energetic'},
    'fanta': {'fanta', 'naranja'},
    'sprite':{'spray','split','esprite','sprite','pretty','pride','prime'},
    'pap':{'pap','papá','papaya','papa'},
    'bilz':{'bill', 'bilz', 'bills','vil','bici'},
    'gracias':{'gracias'},
    #'hola': {'hola','buenas', 'buenos días', 'buenas tardes', 'buenas noches', 'hello'},
    'confirmar':{'si','ya','por supuesto', 'por que no', 'dale','obvio','afirmativo','posivio'},
    'comprar':{'compra','comprar'},
    #'comprar':{'comprar', 'dame', 'quiero','tienes'}
     }

    # Building dictionary of Intents & Keywords
    keywords={}
    keywords_dict={}

    for k in list_syn.keys():
        keywords[k]=[]
        for synonym in list(list_syn[k]):
            keywords[k].append('.*\\b'+synonym+'\\b.*')

    for intent, keys in keywords.items():
    # Joining the values in the keywords dictionary with the OR (|) operator updating them in keywords_dict dictionary
        keywords_dict[intent]=re.compile('|'.join(keys))

    responses={
        'hola':'Muy buenas noches estimado cliente',
        'cocacola':'Quieres una cocacola original o zero',
        'kem':'Quieres una Kem energética o Piña',
        'zero':'Va una coca zero entonces',
        'original':'Va una coca original entonces',
        'piña':'Ok, va una Kem piña.',
        'xtream':'Ok, Kem energética.',
        'fanta': 'Lo siento no tengo fanta',
        '7up': 'Vale, una seven up entonces.',
        'pap':' va una sabor pa pa ya',
        'bilz': 'Va una bilz',
        'pepsi': 'Va una Pepsi, heladita',
        'sprite': 'dale, una sprite.',
        'fallback':'disculpa, no entendí.',
        'confirmar':'Entendido',
        'gracias':'de nada',
        'comprar':'Excelente, procedemos a la compra.'
        }

    def chat(entrada):
        # Takes the user input and converts all characters to lowercase
        user_input = entrada.lower()
        
        matched_intent = None 
        
        for intent,pattern in keywords_dict.items():
            
            # Using the regular expression search function to look for keywords in user input
            if re.search(pattern, user_input): 
                
                # if a keyword matches, select the corresponding intent from the keywords_dict dictionary
                matched_intent=intent  
                #print(matched_intent)
        
        # The fallback intent is selected by default
        key='fallback' 
        if matched_intent in responses:
            
            # If a keyword matches, the fallback intent is replaced by the matched intent as the key for the responses dictionary
            key = matched_intent 
        return responses[key], key

    if request.method == 'GET':
        mensaje = request.GET['mensaje']
        #resp = chatbot.get_response(mensaje)
        #print("in:",mensaje,"\nout:",resp, type(resp))
        resp, key = chat(mensaje)
        desc = {
                'respuesta':str(resp),
                'produc':key,
                }

    return JsonResponse(desc)

    def csrf_failure(request, reason=""):
        pass