from django.contrib import admin

from .models import Conta, Categoria
# Register your models here.

admin.site.register(Conta)
admin.site.register(Categoria)