from .linkedin_json_data import create_text_post, create_article_post, register_upload_and_share_image
from .models import Post

def hace_publicacion_cola():
    posts = Post.objects.filter(publicado=False).filter(rrss='LN')
    if posts.count():
        post = posts[0]
        text_content = str(post.contenido) + "\nFuente: {}".format(post.fuente)  
        result = register_upload_and_share_image(image_share_text=text_content, image_title="titulo img ", image_path=post.image_url.path)
        post.publicado=True
        post.save()
        return result

