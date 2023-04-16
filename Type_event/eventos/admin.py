from django.contrib import admin

# Register your models here.

from .models import Evento

# adicionando no painel administrativo
admin.site.register(Evento)