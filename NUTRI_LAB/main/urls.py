from django.urls import path
from . import views

urlpatterns=[
    path('patient/', views.patient, name='patient'),
    path('config_patient/<str:id>/', views.config_patient, name='config_patient'),
    path('edit_patient/<str:id>/', views.edit_patient, name='edit_patient'),

    path('patient_data/', views.patient_data_list, name="patient_data_list"),
    path('patient_data/<str:id>/', views.patient_data, name="patient_data"),
    path('graphic_patient/<str:id>/', views.graphic_kg, name="graphic_patient"),

    path('food_plan/', views.food_plan_list, name="food_plan_list"),
    path('food_plan/<str:id>/', views.food_plan, name="food_plan"),
    path('food/<str:id_paciente>/', views.food, name="food"),
    path('options/<str:id_paciente>/', views.options, name="options"),

]