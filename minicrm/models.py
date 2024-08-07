from django.db import models


class Estado(models.Model):
    estado = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return self.estado 
    
class Contact(models.Model):
    full_name = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    organization = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    status = models.ForeignKey("Estado", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name or f"{self.first_name} {self.last_name}".strip()

    class Meta:
        ordering = ['last_name', 'first_name']
        
