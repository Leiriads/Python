from django.db import models
from datetime import datetime
from django.db.models import Sum

# Create your models here.

class Categoria(models.Model):
    categoria = models.CharField(max_length=50)
    essencial = models.BooleanField(default=False)
    valor_planejamento = models.FloatField(default=0)
    
    def __str__(self):
        return self.categoria

    def total_gasto(self):
        from extrato.models import Valores
        valores = Valores.objects.filter(categoria__id = self.id).filter(data__month=datetime.now().month).aggregate(Sum('valor'))
        return valores['valor__sum'] if valores['valor__sum'] else 0

    def calcula_percentual_gasto_por_categoria(self):
        #Adicione o try para evitar o ZeroDivisionError (Erro de divisão por zero)
        try:
            return int((self.total_gasto() * 100) / self.valor_planejamento)
        except:
            return 0
        
    def total(self):
        from extrato.models import Valores
        valores = Valores.objects.filter(categoria__id = self.id).filter(data__month=datetime.now().month).aggregate(Sum('valor'))
        print(valores)
        return valores['valor__sum'] if valores['valor__sum'] else 0
    
    def somar_valores(self):
        from extrato.models import Valores
        categorias = Categoria.objects.all()
        total = 0

        for categoria in categorias:
            valores = Valores.objects.filter(categoria__id=categoria.id).filter(data__month=datetime.now().month).aggregate(Sum('valor'))
            total += valores['valor__sum'] if valores['valor__sum'] else 0
        print(total)
        return total
    



class Conta(models.Model):
    banco_choices = (
        ('NU', 'Nubank'),
        ('CE', 'Caixa econômica'),
    )

    tipo_choices = (
        ('pf', 'Pessoa física'),
        ('pj', 'Pessoa jurídica'),
    )

    apelido = models.CharField(max_length=50)
    banco = models.CharField(max_length=2, choices=banco_choices)
    tipo = models.CharField(max_length=2, choices=tipo_choices)
    valor = models.FloatField()
    icone = models.ImageField(upload_to='icones')

    def __str__(self):
        return self.apelido