import pandas as pd
from dateutil.parser import parse
import pytz
import xml.etree.ElementTree as ET
import json
import feedparser
import re
import time
from bs4 import BeautifulSoup
import json
import requests
from .models import Fuentes, Contenido
from datetime import datetime, timezone


def extraer_contenido(feed_url):
    # Analizar el feed RSS
    feed = feedparser.parse(feed_url)

    # Lista para almacenar los resultados
    resultados = []

    # Recorrer las entradas del feed
    for entry in feed.entries:
        # Obtener el título
        titulo = entry.title
        if 'published' in entry:
            published = entry.published
        elif 'updated' in entry:
            published = entry.updated
        else:
            published= ""
        # Obtener el contenido
        if 'content' in entry:
            contenido = entry.content[0].value
        elif 'summary' in entry:
            contenido = entry.summary
        else:
            contenido = ""

        # Obtener el enlace
        try:
            enlace = entry.link

            # Agregar los resultados a la lista
            #resultados.append({'titulo': titulo, 'contenido': contenido, 'enlace': enlace})
            resultados.append({ 'enlace': enlace, 'published':published, 'titulo': titulo})
        except:
            pass

    return resultados

def extract_json_blobs(content):
    i = 0
    while i < len(content):
        if content[i] == '{':
            for j in range(len(content) - 1, i, -1):
                if content[j] == '}':
                    try:
                        yield json.loads(content[i:j+1])
                        i = j
                        break
                    except json.JSONDecodeError as e:
                        pass
        i += 1



def get_json_from_url(url): 
    # Consulta la lista de publicaciones actual
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch data from URL. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_last_id_from_json(data):
    #devuelve el ultimo id de la lista de publicaciones
    try:
        # Sort the data by id in descending order
        sorted_data = sorted(data, key=lambda x: x['id'], reverse=True)
        # Return the id of the first item in the sorted data
        return sorted_data[0]['id']
    except Exception as e:
        print(f"Error: {e}")
        print("poner 0")
        return 0 
    
def obtener_nombre_extension(url):
    # Patrón para extraer el nombre de la imagen y su extensión
    patron = r'/([^/]+)\.(jpg|jpeg|png|gif|bmp|svg|webp|tiff|ico)(\?.*)?$'
    # Buscar coincidencias en la URL
    coincidencias = re.search(patron, url)
    
    if coincidencias:
        # Extraer el nombre y la extensión de la imagen
        nombre_imagen = coincidencias.group(1)
        extension = coincidencias.group(2)
        return nombre_imagen, extension
    else:
        timestamp = int(time.time())
        # Convertir el timestamp a una cadena de caracteres
        timestamp_str = str(timestamp)
        return timestamp_str, 'jpg'
    
def open_graph(link):
    # Rescata los metadatos del articulo incluido la imágen principal
    print(link)
    response = requests.get(link)
    #response.raise_for_status()  # Raise an exception for any HTTP errors
    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.content, 'html.parser')
    opengraph = {"tipo":"og:type","titulo":"og:title","url":"og:url","imagen":"og:image"}
    metadata = {}
    for og in opengraph.keys():
        try:
            metadata[og]=soup.find("meta", property=opengraph[og])['content']
        except:
            metadata[og]=''
    metadata['imagen']
    return metadata

def descargar_imagen(url, nombre_archivo):
    try:
        # Realizar la solicitud GET a la URL
        respuesta = requests.get(url)
        # Verificar si la solicitud fue exitosa (código de estado 200)
        if respuesta.status_code == 200:
            # Guardar la imagen en un archivo local
            with open(nombre_archivo, 'wb') as archivo:
                archivo.write(respuesta.content)
            print(f"La imagen ha sido descargada como '{nombre_archivo}'")
        else:
            print(f"Error al descargar la imagen. Código de estado: {respuesta.status_code}")
    except Exception as e:
        print(f"Ocurrió un error: {str(e)}")

# #Abre archivo de fuentes de datos RSS
# json_file = "fuentes_rss.json"
# with open(json_file, 'r') as f:
#     data = json.load(f)

def proceso_diario():
    # # Proceso que recolecta las noticias diarias
    fuentes = Fuentes.objects.all()
    for f in fuentes:
        contenido_feed = extraer_contenido(f.url)  
        if contenido_feed !=[]:
            for entrada in contenido_feed:
                publicada = entrada['published']
                if publicada == '':
                    pass
                else:
                    enlace = entrada['enlace']
                    publicado = parse(publicada).replace(tzinfo=pytz.UTC)
                    titulo = entrada['titulo']
                    contenido = Contenido(enlace=enlace,publicado=publicado,titulo=titulo , fuente= f)
                    try:
                        contenido.save()
                    except:
                        pass
        else:
            f.estado=False
            f.save()
                
    print("Listo!")

def revisa_multimedia():
    #Filtros y orden
    hoy=datetime.date(datetime.now(timezone.utc))
    contenidos = Contenido.objects.filter(publicado__gte=hoy)
    for j,cont in enumerate(contenidos):
        try:
            print(cont.enlace)
            response = requests.get(cont.enlace, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')
            img_link = soup.find("meta", property="og:image")
            if img_link is not None:
                cont.imagen = img_link['content']
                cont.save()
                print("multimedia {}/{}".format(j, contenidos.count()))
            else: 
                print("NA")
            
        except requests.Timeout:
            # Maneja la situación de tiempo de espera aquí
            print("La solicitud ha excedido el tiempo de espera.")
        except requests.RequestException as e:
            # Maneja otras excepciones de la solicitud aquí
            print("Error en la solicitud:", e)


