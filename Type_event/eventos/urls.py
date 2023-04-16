from django.urls import path
from . import views

urlpatterns = [
    path('novo_evento/', views.novo_evento, name="novo_evento"),
    path('gerenciar_evento/', views.gerenciar_evento, name="gerenciar_evento"),
    path('inscrever_evento/<int:id>/', views.inscrever_evento, name="inscrever_evento"),
    path('participantes_evento/<int:id>/', views.participantes_evento, name="participantes_evento"),
    path('gerar_csv/<int:id>/', views.gerar_csv, name="gerar_csv"),
]