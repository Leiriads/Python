from django.urls import path
from . import views

urlpatterns=[
    path('patient/', views.patient, name='patient'),
    path('patient_data/', views.patient_data_list, name="patient_data_list"),
    path('patient_data/<str:id>/', views.patient_data, name="patient_data"),
    path('graphic_patient/<str:id>/', views.graphic_kg, name="graphic_patient")

]