import requests
from .models import Post

def publica_ig(image_url,caption):
    # URL y token de acceso
    ig_user_id = 17841437330746998
    media_url = "https://graph.facebook.com/v19.0/{}/media".format(ig_user_id)
    publish_url = "https://graph.facebook.com/v19.0/{}/media_publish".format(ig_user_id)
    access_token = "EAALHkpR0WOABO0eJRrMZBDbE2qnZBZAwQMuUzA7ZCsfSxXeL9f94PD6gZAuOoCB9x1nZAZCTeldlkLJ4j4KpZA2I9tNEskDF0jgjKzWGFR2ggvwSoaielTZAorksxmCaa1S0kxXQDnmw9SUrZBflD6eDZAAgQCZCiwvwZAzERtFpPq8j0FjuHMu3WoQGZCZARUFl5W3IJ4zZCaZC2EcW9zQZDZD"

    # Realizar la solicitud POST para subir la imagen
    media_response = requests.post(media_url, data={"image_url": image_url, "caption":caption, "access_token": access_token})
    media_data = media_response.json()

    if "id" in media_data:
        creation_id = media_data["id"]
        # Realizar la solicitud POST para publicar la imagen
        publish_response = requests.post(publish_url, data={"creation_id": creation_id, "access_token": access_token})
        print(publish_response.text)
    else:
        print("Error al subir la imagen:", media_data)


def hace_publicacion_ig():
    posts = Post.objects.filter(publicado=False).filter(rrss='IG')
    if posts.count():
        post = posts[0] # toma solo el primer post no publicado 
        text_content = str(post.contenido) #+ "\nFuente: {}".format(post.fuente)  
        result = publica_ig(image_url="http://app.streetflow.cl"+post.image_url.url, caption=text_content, )
        post.publicado=True
        post.save()
        return result