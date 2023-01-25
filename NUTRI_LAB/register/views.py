from django.shortcuts import render
from django.http import HttpResponse
from .utils import password_is_valid
#biblioteca de redirecionamento
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth


# Create your views here.
#return HttpResponse("testando")


def register(request):

    if request.method == 'GET':
        return render(request,'cadastro.html')

    elif request.method == 'POST':
        usuario = request.POST.get('usuario')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not password_is_valid(request, senha, confirmar_senha):
            return redirect('/auth/register')

        try:
            user = User.objects.create_user(username=usuario,
            email=email,
            password=senha,
            is_active=False)
            user.save()
            messages.add_message(request,constants.SUCCESS,'Usuário Cadastrado com sucesso')
            return redirect('/auth/login')
            
        except:
            messages.add_message(request,constants.ERROR,'Erro interno do sistema')
            return redirect('/auth/register')

      

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')

    elif request.method == "POST":
        username = request.POST.get('usuario')
        senha = request.POST.get('senha')
        usuario = auth.authenticate(username=username, password=senha)
        #retorna true ou falso
    if not usuario:
        messages.add_message(request, constants.ERROR, 'Usuário ou senha inválidos')
        return redirect('/auth/login')
    else:
        auth.login(request, usuario)
        return redirect('/')