 
from rest_framework import serializers 
from .models import Post 
  
# class PostSerializer(serializers.ModelSerializer): 
#     class Meta: 
#         model = Post 
#         fields = "__all__"

class PostSerializer(serializers.ModelSerializer): 
    # Add a file field to accept file uploads
    file = serializers.FileField(required=False)
    
    class Meta: 
        model = Post 
        fields = "__all__"