from django.shortcuts import render,redirect

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from .models import Pacientes

@login_required(login_url='/auth/login/')
def patient(request):
    if request.method == "GET":

        pacientes = Pacientes.objects.filter(nutri=request.user)
        return render(request, 'main.html', {'pacientes': pacientes})




        return render(request,'main.html')

    elif request.method == "POST":
        
        nome = request.POST.get('nome')
        sexo = request.POST.get('sexo')
        idade = request.POST.get('idade')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
       

        #.strip tira o espaço em branco

        if (len(nome.strip()) == 0) or (len(sexo.strip()) == 0) or (len(idade.strip()) == 0) or (len(email.strip()) == 0) or (len(telefone.strip()) == 0):
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return redirect('/patient/')

        #se idade nao for numero 
        if not idade.isnumeric():
            messages.add_message(request, constants.ERROR, 'Digite uma idade válida')
            return redirect('/patient/')

        pacientes = Pacientes.objects.filter(email=email)
        #trazer tudo que tenha na tabela paciente , mas apenas o paciente que o email for igual ao email do form
        if pacientes.exists():
            messages.add_message(request, constants.ERROR, 'Já existe um paciente com esse E-mail')
            return redirect('/patient/')



        try:
            paciente = Pacientes(nome = nome,
                                sexo = sexo,
                                idade = idade,
                                email = email,
                                telefone = telefone,
                                nutri = request.user)

            paciente.save()

            messages.add_message(request, constants.SUCCESS, 'Paciente cadastrado com sucesso')
            return redirect('/patient/')
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return redirect('/patient/')

@login_required(login_url='/auth/login/')
def patient_data(request):
    if request.method == "GET":
        pacientes = Pacientes.objects.filter(nutri=request.user)
        return render(request, 'patient_data.html', {'pacientes': pacientes})