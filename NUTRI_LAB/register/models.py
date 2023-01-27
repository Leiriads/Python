from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Activation(models.Model):
    token = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    ativo = models.BooleanField(default=False)
    
    #no terminal
    #python manage.py makemigrations
    #python manage.py migrate
    def __str__(self):
        return self.user.username