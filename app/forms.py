from django import forms
from app.models import Usuario

class formulario(forms.ModelForm):
    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
    )
    confirmar_senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
    )

    class Meta:
        model = Usuario
        fields = (
            'nome', 'email', 'senha', 'confirmar_senha',
            'cep', 'numero'
        )
        labels = {
            'numero': 'Número de residência',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.TextInput(attrs={'type': 'email', 'class': 'form-input'}),
            'cep': forms.TextInput(attrs={'class': 'form-input', 'id': 'cep'}),
            'logradouro': forms.TextInput(attrs={'class': 'form-input', 'id': 'logradouro'}),
            'bairro': forms.TextInput(attrs={'class': 'form-input', 'id': 'bairro'}),
            'localidade': forms.TextInput(attrs={'class': 'form-input', 'id': 'localidade'}),
            'uf': forms.TextInput(attrs={'class': 'form-input', 'id': 'uf'}),
            'numero': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        confirmar_senha = cleaned_data.get("confirmar_senha")

        if senha and confirmar_senha and senha != confirmar_senha:
            self.add_error("confirmar_senha", "As senhas não coincidem.")


from django import forms
from app.models import Usuario

class formLogin(forms.ModelForm):
    class Meta: # não precisa de parenteses
        model = Usuario
        fields = ('email', 'senha')

        widgets = {
            'email' : forms.TextInput(attrs={'type':'email', 'class':'form-input'}),
            'senha' : forms.TextInput(attrs={'type':'senha', 'class':'form-input'})
        }

from django import forms
from app.models import Produto

class formProduto(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ('nome', 'descricao', 'preço', 'estoque', 'imagem')

        widgets = {
            'nome': forms.TextInput(attrs={'type': 'text', 'class': 'form-input'}),
            'descricao': forms.TextInput(attrs={'type': 'text', 'class': 'form-input'}),
            'preço': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-input'}),
            'estoque': forms.NumberInput(attrs={'class': 'form-input'}),
            'imagem': forms.ClearableFileInput(attrs={'accept': 'image/*', 'class': 'form-input'})
        }
