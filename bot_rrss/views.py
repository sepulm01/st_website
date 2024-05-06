from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse 
from django.views.decorators.csrf import csrf_exempt 
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import  ( MultiPartParser, FormParser)
from rest_framework.response import Response  
from rest_framework import viewsets  
from rest_framework import authentication, permissions
from rest_framework.views import APIView

from .models import Post, Contenido
from .serializers import PostSerializer 
from datetime import datetime, timezone, timedelta


class NoticiasView(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


@csrf_exempt
@api_view(['POST','GET'])
@parser_classes([MultiPartParser, FormParser])
def post_feed_endpoint_view(request): 
    """ 
    List all Posts, or create a new Post 
    """
    if request.method == 'GET': 
        post = Post.objects.all() 
        serializer = PostSerializer(post, many=True) 
        return JsonResponse(serializer.data, safe=False) 
  
    elif request.method == 'POST': 
        file = request.FILES.get('file')
        data = request.data
        
        data.pop('file', None)
        non_file_data = {key: value for key, value in data.items() if key != 'file'}
        
        serializer = PostSerializer(data=non_file_data) 
        if serializer.is_valid(): 
            instance = serializer.save() 
            #serializer.save() 
            if file:
                instance.image_url = file
                instance.save()
            return JsonResponse(serializer.data, status=201) 
        print(serializer.errors)
        return JsonResponse(serializer.errors, status=400) 
  

@csrf_exempt
@api_view(['GET'])
def get_noticias_hoy(request):
    """
    Return a list of las noticias del día de hoy. Se usa para q el modelo de llm elija cuales publicar.
    """
    hoy=datetime.date(datetime.now(timezone.utc))
    hoy = hoy - timedelta(hours=24)
    contenidos = Contenido.objects.filter(publicado__gte=hoy, imagen__isnull=False)
    feed = {}
    for cont in contenidos:
        feed[cont.pk]={"tema":cont.fuente.tema, "titulos":cont.titulo, "enlaces":cont.enlace, "fotos": cont.imagen}

    #noticias = ["index:{} {} - titulo: {}, ".format(i.pk,i.fuente,i.titulo) for i in contenidos]
    
    return Response(feed    )

@csrf_exempt
@api_view(['GET'])
def get_noticias_all(request):
    """
    Return a list of todas las noticias de la base
    """
    contenidos = Contenido.objects.all()
    feed = {}
    for cont in contenidos:
        feed[cont.pk]={"tema":cont.fuente.tema, "titulos":cont.titulo, "enlaces":cont.enlace, "fotos": cont.imagen, 'publicado':cont.publicado}

    #noticias = ["index:{} {} - titulo: {}, ".format(i.pk,i.fuente,i.titulo) for i in contenidos]
    
    return Response(feed)

'''
import requests

# URL de la API
url = "http://127.0.0.1:8000/bot_rrss/feed/hoy"

# Realizar la solicitud GET
response = requests.get(url)

# Verificar el estado de la respuesta
if response.status_code == 200:
    # La solicitud fue exitosa
    data = response.json()  # Convertir la respuesta a JSON
    print(data)  # Imprimir los datos obtenidos
else:
    # La solicitud falló
    print("Error al realizar la solicitud. Código de estado:", response.status_code)


'''