from django.contrib import admin

# Register your models here.

#para aparecer a nova tela de activation no admin precisa importar
from .models import Activation
admin.site.register(Activation) 
