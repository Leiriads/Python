from django.urls import path 
from . import views



urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.login, name ="login"),
    path('quit/', views.quit, name="quit"),
    path('activate_account/<str:token>/', views.activate_account, name="activate_account")
]