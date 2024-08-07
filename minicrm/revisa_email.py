
import imaplib
import email
from email import policy
#from email.parser import BytesParser
from email.header import decode_header
import base64, json
from bs4 import BeautifulSoup

import re
import pandas as pd
import random
from .models import *

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
     

api_key = 'hnonDumZKwfndnpVxWuZNYuoaldTwbsW'
model = "open-mistral-7b"
client = MistralClient(api_key=api_key)
clases = ['business_opportunities', 'advertising', 'not_sure', 'spam' , 'customer', 'partner']

def analizar_spam(subject, body=None):
    prompt = """
    You are a junior assistant and employee at a computer vision startup called Recdata. Your boss is Martin Sepulveda. Your duty is to read daily emails You classify them with this criteria:
    - As business opportunities only email that related on securiry systems, quotations, computer vision, and Martín Sepúlveda is involve or named.
    - As advertising any offer, savigs promotion, sales or discount.
    - As spam any linkedin stuff, contact message, job offer etc, 
    - As Facturas any reference in spanish word factura, facturación, etc. or Invoice in english.
    - and I'm not sure, the rest.
    
    You will only respond with a JSON object with the key classification from this list ['business_opportunities', 'advertising', 'not_sure', 'spam' ] and Confidence. Do not provide explanations.
    """
    messages = [
        ChatMessage(role="system", content=prompt),
        ChatMessage(role="user", content=f"subject: {subject}\n\nbody: {body}")
    ]
    
    chat_response = client.chat(
        model="mistral-tiny",
        messages=messages
    )
    
    # Accedemos directamente al contenido de la respuesta
    resultado = chat_response.choices[0].message.content.strip().lower()
    
    return resultado


#########################
#### Funciones Correo
#########################

def parseohtml(html):
  # Crear un objeto BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Eliminar todos los scripts y estilos
    for script in soup(["script", "style"]):
        script.decompose()

    # Obtener el texto
    texto = soup.get_text()
    
    # Dividir en líneas y eliminar espacios en blanco adicionales
    lineas = (line.strip() for line in texto.splitlines())
    
    # Romper líneas múltiples en una línea cada una
    chunks = (phrase.strip() for line in lineas for phrase in line.split("  "))
    
    # Eliminar líneas en blanco
    texto = '\n'.join(chunk for chunk in chunks if chunk)

    return texto

def extraer_contenido_email(msg):
    contenido = {
        'text': [],
        'html': [],
        'attachments': []
    }

    def extraer_parte(part):
        content_type = part.get_content_type()
        try:
            body = part.get_payload(decode=True).decode()
        except:
            body = part.get_payload()

        if content_type == 'text/plain':
            contenido['text'].append(body)
        elif content_type == 'text/html':
            contenido['html'].append(body)
        elif part.get_filename():
            # Es un archivo adjunto
            filename = decode_header(part.get_filename())[0][0]
            if isinstance(filename, bytes):
                filename = filename.decode()
            contenido['attachments'].append({
                'filename': filename,
                'content': base64.b64encode(part.get_payload(decode=True)).decode(),
                'content_type': content_type
            })

    if msg.is_multipart():
        for part in msg.walk():
            extraer_parte(part)
    else:
        extraer_parte(msg)

    return contenido

def lista_a_string(lista):
    return ' '.join(map(str, lista))

def list_mail_folders(mail):
    # Obtener la lista de carpetas
    status, folders = mail.list()
    lista = []
    if status == 'OK':
        for folder in folders:
            lista.append(folder.decode())
    else:
        print("Failed to retrieve folders.")
    return lista
    
    # Cerrar la conexión
    #mail.logout()
    
def create_mail_folder(mail, folder_name):
    # Crear una carpeta
    status, response = mail.create(folder_name)
    
    if status == 'OK':
        print(f"Folder '{folder_name}' created successfully.")
        return True
    else:
        print(f"Failed to create folder '{folder_name}'. Response: {response}")
        return False
    # Cerrar la conexión
    #mail.logout()
    
def mover_correo(mail, mail_id, carpeta_origen, carpeta_destino):
    # Seleccionar la carpeta de origen
    mail.select(carpeta_origen)
    
    # Obtener el UID del mensaje
    _, msg_data = mail.fetch(mail_id, '(UID)')
    uid = msg_data[0].decode().split()[2][:-1]
    
    # Mover el correo
    result = mail.uid('COPY', uid, carpeta_destino)
    if result[0] == 'OK':
        # Marcar el correo original como eliminado
        mail.uid('STORE', uid, '+FLAGS', '(\Deleted)')
        # Expurgar para eliminar definitivamente
        mail.expunge()
        return True
    return False

def extraer_email(string):
    patron = r'<([^>]+)>'
    match = re.search(patron, string)
    return match.group(1) if match else None

def procesa(server, user, password, registrados):
    mail = imaplib.IMAP4_SSL(server,993)
    mail.login(user, password)
    mail.select('INBOX')
    # Buscar correos (por ejemplo, todos los correos no leídos)
    mail.select('INBOX')
    status, data = mail.search(None, 'UNSEEN')
    mail_ids = data[0].split()
    carpeta_origen="INBOX"
    carpeta_destino="INBOX.spam"
    mover_mail = False
    contactos_procesados = []
    for mail_id in mail_ids:
        try:
            status, msg_data = mail.fetch(mail_id, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1], policy=policy.default)
            subject = msg['subject']
            from_ = msg['from']
            resultado = extraer_contenido_email(msg) #extrae el body
            print(f"\n\nAsunto: {subject}, \nDe: {from_}")
        
            body = parseohtml(lista_a_string(resultado['html']))
            if len(body):
                if from_ in registrados:
                    print("eMail registrado {}".format(from_))
                else:  
                    ia_class = json.loads(analizar_spam(subject,body)) # {'classification': 'business_opportunities', 'confidence': 1.0}
                    print(ia_class)
                    carpeta_destino = "INBOX."+ia_class['classification']
                    print(carpeta_destino)
                    create_mail_folder(mail, carpeta_destino)
                    ia_class['contact']=extraer_email(from_)
                    ia_class['input']='auto'
                    contactos_procesados.append(ia_class)
                    if 1:
                        if mover_correo(mail, mail_id, carpeta_origen, carpeta_destino):
                            print(f"Correo movido: {msg['Subject']}")
                        else:
                            print(f"Error al mover el correo: {msg['Subject']}")
        except:
            pass
    print(contactos_procesados)
    mail.logout()

##############################
#### fin funciones correo
#############################

# Conectarse al servidor de correo
server = 'mail.recdata.cl'
user = 'martin.sepulveda@recdata.cl'
password = 'Rguax910+'

# Lista de tipos de contacto
tipos_contacto = clases
email_registados = Contact.objects.all()
registrados = [x.email for x in email_registados]



