from rest_framework import serializers
from .models import Produto  # Modelo do app

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ('id', 'nome', 'preço', 'estoque', 'imagem') 
