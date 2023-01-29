from django.urls import path
from . import views

urlpatterns=[
    path('patient/', views.patient, name='patient'),
    path('patient_data/', views.patient_data, name="patient_data"),

]