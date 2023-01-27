from django.shortcuts import render
from django.http import HttpResponse
from .utils import password_is_valid, email_html
#biblioteca de redirecionamento
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth
#envio email
import os
from django.conf import settings
#ativacao
from .models import Activation
#hash
from hashlib import sha256

# Create your views here.
#return HttpResponse("testando")


def register(request):

    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
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


            #sha256 precisa de binario, converter string pra binario com .encode o sha retorna um metodo um endereço de memoria
            #converter em hexadecimal com hexdigest
            token = sha256(f"{usuario}{email}".encode()).hexdigest()
    
            activation = Activation(token = token,user=user)
            activation.save()

            path_template = os.path.join(settings.BASE_DIR, 'register/templates/emails/cadastro_confirmado.html')
            email_html(path_template, 'Cadastro confirmado', [email,], username=usuario, link_ativacao=f"127.0.0.1:8000/auth/activate_account/{token}")

            messages.add_message(request,constants.SUCCESS,'Usuário Cadastrado com sucesso')
            return redirect('/auth/login')
            
        except:
            messages.add_message(request,constants.ERROR,'Erro interno do sistema')
            return redirect('/auth/register')

      

def login(request):
    if request.method == "GET":
        #se esta autenticado retorna pra main
        if request.user.is_authenticated:
            return redirect('/')

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


def quit(request):
    auth.logout(request)
    return redirect('/auth/login')

def activate_account(request, token):
    #getobject busca objeto no banco, se o objeto nao existir retorna um 404
    token = get_object_or_404(Activation, token=token)
    if token.ativo:
        messages.add_message(request, constants.WARNING, 'Essa token já foi usado')
        return redirect('/auth/login')

    #print(token.user.email)
    #return HttpResponse('teste')
    user = User.objects.get(username=token.user.username)
    user.is_active = True
    user.save()
    token.ativo = True
    token.save()
    messages.add_message(request, constants.SUCCESS, 'Conta ativa com sucesso')
    return redirect('/auth/login')