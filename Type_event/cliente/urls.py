from django.urls import path
from . import views

urlpatterns = [
    path('meus_certificados/', views.meus_certificados, name="meus_certificados"),
]