
import re, json
import requests
from bs4 import BeautifulSoup
import time
from .models import Fuentes


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

        
def cargar_fuentes(file='bot_rrss/fuentes_rss.json'):
    #Abre archivo de fuentes de datos RSS
    json_file = file
    with open(json_file, 'r') as f:
        data = json.load(f)

    for t in data.keys():
        for d in data[t]:
            print(t, d['text'],d['title'],d['type'],d['xmlUrl'] )
            fuentes = Fuentes(tema=t,
                    texto=d['text'],
                    titulo=d['title'],
                    tipo = 'RSS',
                    url = d['xmlUrl']
                    )
            fuentes.save()

