from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from .models import Pacientes,DadosPaciente,Refeicao,Opcao
from datetime import datetime
#graphic
from django.views.decorators.csrf import csrf_exempt

from django.contrib import auth

from .forms import PacienteForm

@login_required(login_url='/auth/login/')
def patient(request):
    if request.method == "GET":
        pacientes = Pacientes.objects.filter(nutri=request.user)
        return render(request, 'main.html', {'pacientes': pacientes})

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
def patient_data_list(request):
    if request.method == "GET":
        pacientes = Pacientes.objects.filter(nutri=request.user)
        return render(request, 'patient_data_list.html', {'pacientes': pacientes})


@login_required(login_url='/auth/login/')
def patient_data(request, id):
    #se nao existe no banco retorna 404
    
    paciente = get_object_or_404(Pacientes,id=id)

    if not paciente.nutri == request.user:
        messages.add_message(request, constants.ERROR, 'Esse paciente não é seu')
        return redirect('/patient_data/')
        
    if request.method == "GET":

        dados_paciente = DadosPaciente.objects.filter(paciente=paciente)
        return render(request, 'patient_data.html', {'paciente': paciente, 'dados_paciente': dados_paciente})

    elif request.method == "POST":
        peso = request.POST.get('peso')
        altura = request.POST.get('altura')
        gordura = request.POST.get('gordura')
        musculo = request.POST.get('musculo')
        hdl = request.POST.get('hdl')
        ldl = request.POST.get('ldl')
        colesterol_total = request.POST.get('ctotal')
        triglicerídios = request.POST.get('triglicerídios')

        if (len(peso.strip()) == 0) or (len(altura.strip()) == 0) or (len(gordura.strip()) == 0) or (len(musculo.strip()) == 0) or (len(hdl.strip()) == 0) or (len(ldl.strip()) == 0) or (len(colesterol_total.strip()) == 0) or (len(triglicerídios.strip()) == 0):
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return redirect('/patient_data/')
   
        elif not peso.isnumeric():
            messages.add_message(request, constants.ERROR, 'Preencha o campo Peso corretamente!')
            return redirect('/patient_data/')
        elif not altura.isnumeric():
            messages.add_message(request, constants.ERROR, 'Preencha o campo Altura corretamente!')
            return redirect('/patient_data/')
        elif not gordura.isnumeric():
            messages.add_message(request, constants.ERROR, 'Preencha o campo Gordura corretamente!')
            return redirect('/patient_data/')
        elif not musculo.isnumeric():
            messages.add_message(request, constants.ERROR, 'Preencha o campo Musculo corretamente!')
            return redirect('/patient_data/')
        elif not hdl.isnumeric():
            messages.add_message(request, constants.ERROR, 'Preencha o campo Hdl corretamente!')
            return redirect('/patient_data/')
        elif not ldl.isnumeric():
            messages.add_message(request, constants.ERROR, 'Preencha o campo Ldl corretamente!')
            return redirect('/patient_data/')
        elif not colesterol_total.isnumeric():
            messages.add_message(request, constants.ERROR, 'Preencha o campo Colesterol corretamente!')
            return redirect('/patient_data/')
        elif not triglicerídios.isnumeric():
            messages.add_message(request, constants.ERROR, 'Preencha o campo Triglicerídios corretamente!')
            return redirect('/patient_data/')
        
        paciente = DadosPaciente(paciente=paciente,
                data=datetime.now(),
                peso=peso,
                altura=altura,
                percentual_gordura=gordura,
                percentual_musculo=musculo,
                colesterol_hdl=hdl,
                colesterol_ldl=ldl,
                colesterol_total=colesterol_total,
                trigliceridios=triglicerídios)

        paciente.save()

        messages.add_message(request, constants.SUCCESS, 'Dados cadastrado com sucesso')

        return redirect('/patient_data/')


@login_required(login_url='/auth/login/')
@csrf_exempt
def graphic_kg(request, id):
    paciente = Pacientes.objects.get(id=id)
    #ordenando os pesos pela data
    dados = DadosPaciente.objects.filter(paciente=paciente).order_by("data")
    #cria uma lista de pesos
    pesos = [dado.peso for dado in dados]
    labels = list(range(len(pesos)))
    data = {'peso': pesos,
            'labels': labels}
    return JsonResponse(data)


def food_plan_list(request):
    if request.method == "GET":
        pacientes = Pacientes.objects.filter(nutri=request.user)
        return render(request, 'food_plan_list.html', {'pacientes': pacientes})


def food_plan(request, id):
    paciente = get_object_or_404(Pacientes, id=id)
    if not paciente.nutri == request.user:
        messages.add_message(request, constants.ERROR, 'Esse paciente não é seu')
        return redirect('/food_plan/')

    if request.method == "GET":

        #ordenando as refeições pelo horario
        r1 = Refeicao.objects.filter(paciente=paciente).order_by('horario')
        #opções
        opcao = Opcao.objects.all()

        return render(request, 'food_plan.html', {'paciente': paciente,'refeicao':r1,'opcao':opcao})




def food(request, id_paciente):
    paciente = get_object_or_404(Pacientes, id=id_paciente)
    if not paciente.nutri == request.user:
        messages.add_message(request, constants.ERROR, 'Esse paciente não é seu')
        return redirect('/patient_data/')

    if request.method == "POST":
        titulo = request.POST.get('titulo')
        horario = request.POST.get('horario')
        carboidratos = request.POST.get('carboidratos')
        proteinas = request.POST.get('proteinas')
        gorduras = request.POST.get('gorduras')

        r1 = Refeicao(paciente=paciente,
                      titulo=titulo,
                      horario=horario,
                      carboidratos=carboidratos,
                      proteinas=proteinas,
                      gorduras=gorduras)

        r1.save()

        messages.add_message(request, constants.SUCCESS, 'Refeição Cadastrada')
        return redirect(f'/food_plan/{id_paciente}')


def options(request, id_paciente):
     if request.method == "POST":

        id_refeicao = request.POST.get('refeicao')
        #tipo arquivo recebe atraves do files
        # no html precisa ter o enctype='multipart/form-data p/ o formulario enviar arquivos
        imagem = request.FILES.get('imagem')
        descricao = request.POST.get("descricao")

        o1 = Opcao(refeicao_id=id_refeicao,
                   imagem=imagem,
                   descricao=descricao)

        o1.save()

        messages.add_message(request, constants.SUCCESS, 'Opcao Cadastrada !')
        return redirect(f'/food_plan/{id_paciente}')




@login_required(login_url='/auth/login/')
def config_patient(request, id):
    paciente = get_object_or_404(Pacientes, id=id)
    if not paciente.nutri == request.user:
        messages.add_message(request, constants.ERROR, 'Esse paciente não é seu')
        return redirect('/patient/')


    if request.method == "GET":

        return render(request, 'patient_settings.html', {'paciente': paciente})
    

    elif request.method == "POST":
    
        username = request.POST.get('usuario')
        senha = request.POST.get('senha')
        usuario = auth.authenticate(username=username, password=senha)

    if not usuario:
        messages.add_message(request, constants.ERROR, 'Usuário ou senha inválidas')
        return redirect(f'/config_patient/{id}')
    else:
        auth.login(request, usuario)
        messages.add_message(request, constants.SUCCESS, 'Paciente Deletado com Sucesso!')
        paciente.delete();

        return redirect('/patient')


@login_required(login_url='/auth/login/')
def edit_patient(request,id):
    paciente = get_object_or_404(Pacientes, id=id)
    if not paciente.nutri == request.user:
        messages.add_message(request, constants.ERROR, 'Esse paciente não é seu')
        return redirect('/patient_data/')

    if request.method == "POST":
        paciente = Pacientes.objects.get(id=id)
        novo_nome = request.POST.get('nome')
        novo_sexo = request.POST.get('sexo')
        novo_idade = request.POST.get('idade')
        novo_email = request.POST.get('email')
        novo_telefone = request.POST.get('telefone')
        
        
        try: 
            paciente = Pacientes.objects.get(id=id)

            paciente.nome= novo_nome
            paciente.sexo = novo_sexo
            paciente.idade = novo_idade
            paciente.email = novo_email
            paciente.telefone = novo_telefone
         
            paciente.save()
            messages.add_message(request, constants.SUCCESS, 'Paciente Alterado com sucesso')
            return redirect('/patient/')
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return redirect('/patient/')

    return


def create_patiente(request):
    form = PacienteForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('patient')
    return render(request,'main.html',{'form':form})


from django.shortcuts import render
import matplotlib.pyplot as plt
import mpld3
from mpld3 import plugins
import random

""" 
def grafico_interativo(request):
    # Coordenadas dos pontos
    coordenadas = [
        (54.425403225806434, 150.86975806451608),
        (129.69354838709677, 150.86975806451608),
        (320.9153225806451, 150.86975806451608),
        (514.171370967742, 150.86975806451608),
        (807.1068548387096, 266.8233870967741),
        (518.2399193548387, 401.08548387096766),
        (322.94959677419354, 399.0512096774193),
        (127.65927419354836, 399.0512096774193),
        (56.45967741935482, 399.0512096774193)
    ]

    # Nomes aleatórios para os pontos
    nomes = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Heidi', 'Ivan']
    random.shuffle(nomes)

    # Mapeamento de nomes para pontos
    nome_map = {}
    for i, ponto in enumerate(coordenadas):
        nome_map[nomes[i]] = ponto

    # Criar o gráfico
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    plt.axis('off')

    # Adicionar os pontos ao gráfico
    points = []
    for nome, ponto in nome_map.items():
        points.append(ax.plot(ponto[0], ponto[1], 'ro')[0])
        plt.text(ponto[0], ponto[1], nome, color='black', fontsize=8, ha='right', va='bottom')

    # Traçar as linhas entre os pontos
    for i in range(len(coordenadas) - 1):
        plt.plot([coordenadas[i][0], coordenadas[i+1][0]], [coordenadas[i][1], coordenadas[i+1][1]], 'r-')

    # Adicionar a última linha que conecta o último ponto ao primeiro ponto
    plt.plot([coordenadas[1][0], coordenadas[7][0]], [coordenadas[1][1], coordenadas[7][1]], 'r-')

    # Converter o gráfico matplotlib em um gráfico interativo em HTML
    html = mpld3.fig_to_html(fig)

    # Passar os nomes das variáveis como contexto adicional
    context = {
        'html': html,
        'nomes_variaveis': nomes,
    }

    return render(request, 'grafico_interativo.html', context)
"""

from django.shortcuts import render
import random

def grafico_interativo(request):
    coordenadas = [
        (54.425403225806434, 150.86975806451608),
        (129.69354838709677, 150.86975806451608),
        (320.9153225806451, 150.86975806451608),
        (514.171370967742, 150.86975806451608),
        (807.1068548387096, 266.8233870967741),
        (518.2399193548387, 401.08548387096766),
        (322.94959677419354, 399.0512096774193),
        (127.65927419354836, 399.0512096774193),
        (56.45967741935482, 399.0512096774193)
    ]

    nomes = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Heidi', 'Ivan']
    cores = ['red', 'yellow', 'yellow', 'yellow', 'red', 'red', 'green', 'green', 'green']

    nome_cor_map = {}
    for i, ponto in enumerate(coordenadas):
        cor = cores[i % len(cores)]
        nome_cor_map[nomes[i]] = {
            'ponto': ponto,
            'cor': cor
        }

    context = {
        'nomes_variaveis': nomes,
        'nome_cor_map': nome_cor_map,
        'cores_linhas': cores  # Adiciona a lista de cores ao contexto
    }

    return render(request, 'grafico_interativo.html', context)


from django.shortcuts import render
import json

def equipamentos_view(request):
    # Seu JSON com os dados dos equipamentos

    equipamentos_json= """
{

  "Anel_25_HM": {

    "quantidade_equipamentos": 1,

    "equipamentos": [

      {

        "equipamento": "SW-MGBHE_O1B64",

        "host": "SW-MGBHE_O1B64",

        "alertas": [

          {

            "clock": "2024-04-10 16:50:35",

            "subject": "EVENTO-INICIADO",

            "duration": "6h 52m 0s",

            "event": "Cisco IOS: Unavailable by ICMP ping",

            "host": "SW-MGBHE_O1B64",

            "severity": "High",

            "time": "Up (1)",

            "problem_id": "484787",

            "Consulta_TA": "MGBHE_O1B64"

          }

        ],

        "ids_consultas": [

          313617946

        ]

      }

    ]

  },

  "Anel_18_HM": {

    "quantidade_equipamentos": 9,

    "equipamentos": [

      {

        "equipamento": "SW-MGBHE_O1B33",

        "host": "SW-MGBHE_O1B33",

        "alertas": [

          {

            "clock": "2024-04-10 20:57:13",

            "subject": "EVENTO-INICIADO",

            "duration": "Inicio : 2024.04.10 \u00e1s 20:57:11",

            "event": "Inicio : 2024.04.10 \u00e1s 20:57:11",

            "host": "SW-MGBHE_O1B33",

            "severity": "Average",

            "time": "Inicio : 2024.04.10 \u00e1s 20:57:11",

            "problem_id": "503392",

            "Consulta_TA": "MGBHE_O1B33"

          }

        ],

        "ids_consultas": []

      },

      {

        "equipamento": "SW-MGBHE_O1B52",

        "host": "SW-MGBHE_O1B52",

        "alertas": [

          {

            "clock": "2024-04-08 11:49:08",

            "subject": "EVENTO-NORMALIZADO",

            "duration": "1m 4s",

            "event": "Interface Slot1/2/2(RT:CONN:TO:BHE-HMT18:SW-MGBHE_O1B48:Xg1/2/1): Link down",

            "host": "SW-MGBHE_O1B52",

            "severity": "Average",

            "time": "Current state: up (1)",

            "problem_id": "426289",

            "Consulta_TA": "MGBHE_O1B52"

          }

        ],

        "ids_consultas": []

      },

      {

        "equipamento": "SW-MGBHE_O1B48",

        "host": "SW-MGBHE_O1B48",

        "alertas": [

          {

            "clock": "2024-04-10 15:40:54",

            "subject": "EVENTO-NORMALIZADO",

            "duration": "1m 0s",

            "event": "Cisco IOS: Unavailable by ICMP ping",

            "host": "SW-MGBHE_O1B48",

            "severity": "High",

            "time": "Up (1)",

            "problem_id": "493753",

            "Consulta_TA": "MGBHE_O1B48"

          }

        ],

        "ids_consultas": []

      },

      {

        "equipamento": "SW-MGBHE_O1B29",

        "host": "SW-MGBHE_O1B29",

        "alertas": [

          {

            "clock": "2024-04-10 20:07:28",

            "subject": "EVENTO-NORMALIZADO",

            "duration": "1m 0s",

            "event": "Interface Slot1/2/20(MGMT:FONTE): Link down",

            "host": "SW-MGBHE_O1B29",

            "severity": "Average",

            "time": "Current state: up (1)",

            "problem_id": "502416",

            "Consulta_TA": "MGBHE_O1B29"

          }

        ],

        "ids_consultas": []

      },

      {

        "equipamento": "SW-MGBHE_O1B51-02",

        "host": "SW-MGBHE_O1B51-02",

        "alertas": [

          {

            "clock": "2024-04-10 18:07:40",

            "subject": "EVENTO-NORMALIZADO",

            "duration": "4m 2s",

            "event": "Cisco IOS: Unavailable by ICMP ping",

            "host": "SW-MGBHE_O1B51-02",

            "severity": "High",

            "time": "Up (1)",

            "problem_id": "499167",

            "Consulta_TA": "MGBHE_O1B51-02"

          }

        ],

        "ids_consultas": []

      },

      {

        "equipamento": "SW-MGBHE_O1B32",

        "host": "SW-MGBHE_O1B32",

        "alertas": [

          {

            "clock": "2024-04-10 17:58:20",

            "subject": "EVENTO-NORMALIZADO",

            "duration": "1m 0s",

            "event": "Interface Slot1/2/2(RT:CONN:TO:HE:BHE-HMT18:SW-MGBHE_HM01_8665:xe3/1/4:ITXATELBHEHM01): Link down",

            "host": "SW-MGBHE_O1B32",

            "severity": "Average",

            "time": "Current state: up (1)",

            "problem_id": "498960",

            "Consulta_TA": "MGBHE_O1B32"

          }

        ],

        "ids_consultas": [

          314070388,

          314055576,

          313896554,

          312781948

        ]

      },

      {

        "equipamento": "SW-MGBHE_O1B31",

        "host": "SW-MGBHE_O1B31",

        "alertas": [

          {

            "clock": "2024-04-10 07:15:13",

            "subject": "EVENTO-NORMALIZADO",

            "duration": "1m 0s",

            "event": "Interface Slot1/2/20(MGMT:FONTE): Link down",

            "host": "SW-MGBHE_O1B31",

            "severity": "Average",

            "time": "Current state: up (1)",

            "problem_id": "481762",

            "Consulta_TA": "MGBHE_O1B31"

          }

        ],

        "ids_consultas": []

      },

      {

        "equipamento": "SW-MGBHE_O1B30",

        "host": "SW-MGBHE_O1B30",

        "alertas": [

          {

            "clock": "2024-04-09 14:35:19",

            "subject": "EVENTO-NORMALIZADO",

            "duration": "1m 0s",

            "event": "Interface Slot1/2/26(MGMT:FONTE): Link down",

            "host": "SW-MGBHE_O1B30",

            "severity": "Average",

            "time": "Current state: up (1)",

            "problem_id": "464095",

            "Consulta_TA": "MGBHE_O1B30"

          }

        ],

        "ids_consultas": []

      },

      {

        "equipamento": "SW-MGBHE_O1B49",

        "host": "SW-MGBHE_O1B49",

        "alertas": [

          {

            "clock": "2024-04-10 15:46:59",

            "subject": "EVENTO-NORMALIZADO",

            "duration": "6m 1s",

            "event": "Cisco IOS: Unavailable by ICMP ping",

            "host": "SW-MGBHE_O1B49",

            "severity": "High",

            "time": "Up (1)",

            "problem_id": "493776",

            "Consulta_TA": "MGBHE_O1B49"

          }

        ],

        "ids_consultas": []

      }

    ]

  },

  "Anel_3_HM": {

    "quantidade_equipamentos": 4,

    "equipamentos": [

      {

        "equipamento": "SW-MGBHE_O1A72",

        "host": "SW-MGBHE_O1A72",

        "alertas": [

          {

            "clock": "2024-04-10 17:47:11",

            "subject": "EVENTO-NORMALIZADO",

            "duration": "2m 0s",

            "event": "Interface Slot1/2/1(RT:CONN:TO:BHE-HMT03:SW-MGBHE_O1A73:Xg1/2/2): Link down",

            "host": "SW-MGBHE_O1A72",

            "severity": "Average",

            "time": "Current state: up (1)",

            "problem_id": "498403",

            "Consulta_TA": "MGBHE_O1A72"

          }

        ],

        "ids_consultas": [

          312746449

        ]

      },

      {

        "equipamento": "SW-MGBHE_O1A73",

        "host": "SW-MGBHE_O1A73",

        "alertas": [

          {

            "clock": "2024-04-10 17:49:41",

            "subject": "EVENTO-NORMALIZADO",

            "duration": "41s",

            "event": "Interface Slot1/2/2(RT:CONN:TO:BHE-HMT03:SW-MGBHE_O1A72:Xg1/2/1): Link down",

            "host": "SW-MGBHE_O1A73",

            "severity": "Average",

            "time": "Current state: up (1)",

            "problem_id": "498472",

            "Consulta_TA": "MGBHE_O1A73"

          }

        ],

        "ids_consultas": [

          312746452

        ]

      },

      {

        "equipamento": "SW-MGBHE_O1A61",

        "host": "SW-MGBHE_O1A61",

        "alertas": [

          {

            "clock": "2024-04-09 13:33:18",

            "subject": "EVENTO-NORMALIZADO",

            "duration": "34m 59s",

            "event": "Cisco IOS: Unavailable by ICMP ping",

            "host": "SW-MGBHE_O1A61",

            "severity": "High",

            "time": "Up (1)",

            "problem_id": "460493",

            "Consulta_TA": "MGBHE_O1A61"

          }

        ],

        "ids_consultas": [

          313853040,

          312772922,

          312746451

        ]

      },

      {

        "equipamento": "SW-MGBHE_O1A65-02",

        "host": "SW-MGBHE_O1A65-02",

        "alertas": [

          {

            "clock": "2024-04-09 13:34:18",

            "subject": "EVENTO-NORMALIZADO",

            "duration": "42m 0s",

            "event": "Interface Slot1/2/1(RT:CONN:TO:ARD:BHE-HMT03:SW-MGBHE_O1A61:Xg1/2/2): Link down",

            "host": "SW-MGBHE_O1A65-02",

            "severity": "Average",

            "time": "Current state: up (1)",

            "problem_id": "460291",

            "Consulta_TA": "MGBHE_O1A65-02"

          }

        ],

        "ids_consultas": [

          312772921

        ]

      }

    ]

  }

}



"""
    
    # Converte o JSON para um objeto Python
    equipamentos = json.loads(equipamentos_json)
    
    # Renderiza o template com os dados
    return render(request, 'equipamentos.html', {'equipamentos': equipamentos})
