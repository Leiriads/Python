from django import forms
from .models import Pacientes,DadosPaciente

class PacienteForm(forms.Modelform):
    class Meta:
        model = Pacientes
        fields = "__all__"