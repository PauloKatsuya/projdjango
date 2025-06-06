from django.db import models
from datetime import datetime

# Create your models here.
class Usuario(models.Model): # aqui dizemos que a classe pai Model irá dar herança para a classe usuario
    nome = models.CharField(max_length=100) # varchar, deve especificar o tamanho
    email = models.EmailField()
    senha = models.CharField(max_length=16)
    
    cep = models.CharField(max_length=9)  # Formato 00000-000
    logradouro = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    localidade = models.CharField(max_length=100)  # Cidade
    uf = models.CharField(max_length=2)  # Estado
    numero = models.CharField(max_length=10)  # Número da residência

    #def __str__(self):
        #return f"{self.nome} ({self.email})"

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=300)
    preço = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='imagens/')
    
    #def __str__(self):
        #return f"{self.nome} ({self.descricao})"

class Venda(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    preço = models.DecimalField(max_digits=10, decimal_places=2)
    numero_cartao = models.CharField(max_length=16)
    validade = models.CharField(max_length=5)
    cvv = models.CharField(max_length=4)
    data_compra = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.usuario.nome} comprou {self.produto.nome} em {self.data_compra}"