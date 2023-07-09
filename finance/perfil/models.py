from django.db import models

# Create your models here.

from django.db import models

# Create your models here.

class Categoria(models.Model):
    categoria = models.CharField(max_length=50)
    essencial = models.BooleanField(default=False)
    valor_planejamento = models.FloatField(default=0)

    def __str__(self):
        return self.categoria

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