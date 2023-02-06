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