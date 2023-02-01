from django.urls import path
from . import views

urlpatterns=[
    path('patient/', views.patient, name='patient'),
    path('patient_data/', views.patient_data_list, name="patient_data_list"),
    path('patient_data/<str:id>/', views.patient_data, name="patient_data"),
    path('graphic_patient/<str:id>/', views.graphic_kg, name="graphic_patient"),
    path('food_plan/', views.food_plan_list, name="food_plan_list"),
    path('food_plan/<str:id>/', views.food_plan, name="food_plan"),
    path('food/<str:id_paciente>/', views.food, name="food"),
    path('options/<str:id_paciente>/', views.options, name="options"),

]