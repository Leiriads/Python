from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Conta,Categoria
from extrato.models import Valores
from django.contrib import messages
from django.contrib.messages import constants
from .utils import calcula_total
from django.db.models import Sum
from datetime import datetime

from contas.models import ContaPaga,ContaPagar



# Create your views here.
#Ativar
	# Linux
		# source venv/bin/activate
	# Windows
		# venv\Scripts\Activate
    # Pacotes
        # pip install -r pacotes.txt

def home(request):

    valores = Valores.objects.filter(data__month=datetime.now().month)
    entradas = valores.filter(tipo='E')
    saidas = valores.filter(tipo='S')

    total_entradas = calcula_total(entradas, 'valor')
    total_saidas = calcula_total(saidas, 'valor')

    
    

    contas = Conta.objects.all()
    total_contas = calcula_total(contas,'valor')

    percentual_gastos_essenciais, percentual_gastos_nao_essenciais = calcula_equilibrio_financeiro()

    quantidade_contas_vencidas= contar_contas_vencidas(request)
    contar_contas_p_vencer = contar_contas_para_vencer(request)
   
    return render(request, 'home.html', {'contas': contas, 
                                         'total_contas': total_contas,
                                         'total_entradas':total_entradas,
                                         'total_saidas':total_saidas,
                                         'percentual_gastos_essenciais':int(percentual_gastos_essenciais),
                                         'percentual_gastos_nao_essenciais':int(percentual_gastos_nao_essenciais),
                                         'quantidade_contas_vencidas': quantidade_contas_vencidas,
                                         'contar_contas_p_vencer':contar_contas_p_vencer
                                         })


def gerenciar(request):
    contas = Conta.objects.all()
    #total_contas = contas.aggregate(Sum('valor'))
    total_contas = 0

    total_contas = calcula_total(contas,'valor')

    return render(request, 'gerenciar.html', {'contas': contas, 'total_contas': total_contas})


def cadastrar_banco(request):
    apelido = request.POST.get('apelido')
    banco = request.POST.get('banco')
    tipo = request.POST.get('tipo')
    valor = request.POST.get('valor')
    icone = request.FILES.get('icone')
    
    if len(apelido.strip()) == 0 or len(valor.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
        return redirect('/perfil/gerenciar/')
    
    conta = Conta(
        apelido = apelido,
        banco=banco,
        tipo=tipo,
        valor=valor,
        icone=icone
    )

    conta.save()
    messages.add_message(request, constants.SUCCESS, 'Conta cadastrada com sucesso')
    return redirect('/perfil/gerenciar/')


def deletar_banco(request, id):
    conta = Conta.objects.get(id=id)
    conta.delete()
    
    messages.add_message(request, constants.SUCCESS, 'Conta removida com sucesso')
    return redirect('/perfil/gerenciar/')


def cadastrar_categoria(request):
    nome = request.POST.get('categoria')
    essencial = bool(request.POST.get('essencial'))

    if len(nome.strip()) == 0 or len(nome.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Preencha o Campo corretamente')
        return redirect('/perfil/gerenciar/')

    categoria = Categoria(
        categoria=nome,
        essencial=essencial
    )

    categoria.save()

    messages.add_message(request, constants.SUCCESS, 'Categoria cadastrada com sucesso')
    return redirect('/perfil/gerenciar/')


def gerenciar(request):
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()
    #total_contas = contas.aggregate(Sum('valor'))
    total_contas = 0

    for conta in contas:
        total_contas += conta.valor

    print(total_contas)
    return render(request, 'gerenciar.html', {'contas': contas, 'total_contas': total_contas, 'categorias': categorias})


def update_categoria(request, id):
    categoria = Categoria.objects.get(id=id)

    categoria.essencial = not categoria.essencial

    categoria.save()

    return redirect('/perfil/gerenciar/')


def dashboard(request):
    dados = {}
    categorias = Categoria.objects.all()

    for categoria in categorias:
        dados[categoria.categoria] = Valores.objects.filter(categoria=categoria).aggregate(Sum('valor'))['valor__sum']

    return render(request, 'dashboard.html', {'labels': list(dados.keys()), 'values': list(dados.values())})


def calcula_equilibrio_financeiro():
    gastos_essenciais = Valores.objects.filter(data__month=datetime.now().month).filter(tipo='S').filter(categoria__essencial=True)
    gastos_nao_essenciais = Valores.objects.filter(data__month=datetime.now().month).filter(tipo='S').filter(categoria__essencial=False)

    total_gastos_essenciais = calcula_total(gastos_essenciais, 'valor')
    total_gastos_nao_essenciais = calcula_total(gastos_nao_essenciais, 'valor')

    total = total_gastos_essenciais + total_gastos_nao_essenciais
    try:
        percentual_gastos_essenciais = total_gastos_essenciais * 100 / total
        percentual_gastos_nao_essenciais = total_gastos_nao_essenciais * 100 / total
        
        return percentual_gastos_essenciais, percentual_gastos_nao_essenciais
    except:
        return 0, 0
    

def contar_contas_vencidas(request):
    MES_ATUAL = datetime.now().month
    DIA_ATUAL = datetime.now().day

    contas = ContaPagar.objects.all()

    contas_pagas = ContaPaga.objects.filter(data_pagamento__month=MES_ATUAL).values('conta')

    contas_vencidas = contas.filter(dia_pagamento__lt=DIA_ATUAL).exclude(id__in=contas_pagas)
    quantidade_contas_vencidas = contas_vencidas.count()
    quantidade_contas_vencidas = int(quantidade_contas_vencidas) 

    return quantidade_contas_vencidas

def contar_contas_para_vencer(request):
    MES_ATUAL = datetime.now().month
    DIA_ATUAL = datetime.now().day

    contas = ContaPagar.objects.all()

    contas_pagas = ContaPaga.objects.filter(data_pagamento__month=MES_ATUAL).values('conta')

  
    contas_proximas_vencimento = contas.filter(dia_pagamento__lte = DIA_ATUAL + 5).filter(dia_pagamento__gte=DIA_ATUAL).exclude(id__in=contas_pagas)
    contas_proximas_vencimento = contas_proximas_vencimento.count()
    contas_proximas_vencimento = int(contas_proximas_vencimento) 

    print(contas_proximas_vencimento)
    return contas_proximas_vencimento