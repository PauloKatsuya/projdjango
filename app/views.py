from django.shortcuts import render
from django.shortcuts import redirect
from datetime import timedelta
import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.http import HttpResponse
from django.template import loader
from app.models import Usuario, Produto, Venda
from app.forms import formulario, formLogin, formProduto # type: ignore
import requests
from django.contrib import messages
import io, urllib, base64
import matplotlib.pyplot as plt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProdutoSerializer
from django.db.models import Count
from django.db.models.functions import TruncDate


# Create your views here.

def app(request):

    pagina_main = loader.get_template('index.html')

    return HttpResponse(pagina_main.render())

#USUARIOS EXIBIR
def exibirUsuarios(request):
    if not request.session.get("email"):
        messages.error(request, "Você precisa estar logado para acessar esta página.")
        return redirect("login")
    usuarios = Usuario.objects.all().values()
    return render(request, "usuarios.html", {'listaUsuarios': usuarios})
 # passando os usuarios como parametro para mostrar eles na pagina
                    # {} PARA PASSAR PARA DICIONARIO PQ VEM COMO ARRAY ASSOCIATIVO

# PRODUTOS EXIBIR
def exibirProdutos(request):
    if not request.session.get("email"):
        messages.error(request, "Você precisa estar logado para acessar esta página.")
        return redirect("login")

    produtos = Produto.objects.all()

    # API FAKE STORE
    produtosapi = requests.get("https://fakestoreapi.com/products").json()

    return render(request, "produtos.html", {
        'listaProdutos': produtos,
        'produtosapi': produtosapi
    })



#USUARIO ADD
def addUsuario(request):
    formUsuario = formulario(request.POST or None)
    if request.method == 'POST':
        if formUsuario.is_valid():
            cep = formUsuario.cleaned_data.get('cep')
            endereco = _buscar_endereco_por_cep(cep)
            if endereco is None:
                messages.error(request, 'CEP inválido ou não encontrado. Por favor, verifique e tente novamente.')
                return render(request, 'add-usuario.html', {'form': formUsuario})
  
            formUsuario.instance.logradouro = endereco['logradouro']
            formUsuario.instance.bairro = endereco['bairro']
            formUsuario.instance.localidade = endereco['localidade']
            formUsuario.instance.uf = endereco['uf']

            formUsuario.save()
            return redirect("exibirUsuarios") 

    return render(request, "add-usuario.html", {'form': formUsuario})

#PRODUTOS ADD
def addProduto(request):
    formProd = formProduto(request.POST or None)

    if request.POST: 
        formProd = formProduto(request.POST, request.FILES)
        if formProd.is_valid():
            formProd.save()
            return redirect("exibirProdutos")

    return render(request, "add-produtos.html", {'form': formProd}) # aspas simples no dicionário

#USUARIO DELETE
def excluirUsuario(request, id_usuario):
    usuario = Usuario.objects.get(id=id_usuario)
    usuario.delete()
    return redirect("exibirUsuarios")

#PRODUTOS DELETE
def excluirProduto(request, id_produtos):
    produto = Produto.objects.get(id=id_produtos)
    produto.delete()
    return redirect("exibirProdutos")

#USUARIO EDIT
def editarUsuario(request, id_usuario):
    usuario = Usuario.objects.get(id=id_usuario)
    formEditarUsuario = formulario(request.POST or None, instance=usuario)

    if request.POST:
        if formEditarUsuario.is_valid():
            # Pega o cep enviado no formulário
            cep = formEditarUsuario.cleaned_data.get('cep')

            # Consulta ViaCEP para atualizar os campos de endereço
            resposta = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
            if resposta.status_code == 200:
                dados_cep = resposta.json()
                if 'erro' in dados_cep:
                    # CEP inválido
                    formEditarUsuario.add_error('cep', 'CEP inválido. Por favor, corrija.')
                    return render(request, "editar-usuario.html", {'form': formEditarUsuario})

                # Atualiza os campos do usuário com os dados do ViaCEP
                usuario.logradouro = dados_cep.get('logradouro', '')
                usuario.bairro = dados_cep.get('bairro', '')
                usuario.localidade = dados_cep.get('localidade', '')
                usuario.uf = dados_cep.get('uf', '')
            else:
                formEditarUsuario.add_error('cep', 'Não foi possível consultar o CEP. Tente novamente.')
                return render(request, "editar-usuario.html", {'form': formEditarUsuario})

            # Atualiza o cep e salva o usuário
            usuario.cep = cep
            usuario.numero = formEditarUsuario.cleaned_data.get('numero')  # número continua manual

            usuario.save()
            return redirect("exibirUsuarios")
    else:
        return render(request, "editar-usuario.html", {'form': formEditarUsuario})
    
#PRODUTO EDIT
def editarProduto(request, id_produtos):
    produto = Produto.objects.get(id=id_produtos)
    
    if request.method == 'POST':
        formEditarProduto = formProduto(request.POST, request.FILES, instance=produto)
        if formEditarProduto.is_valid():
            formEditarProduto.save()
            return redirect("exibirProdutos")
    else:
        formEditarProduto = formProduto(instance=produto)
    
    return render(request, "editar-produtos.html", {'form': formEditarProduto})


#LOGIN
def login(request):
    frmLogin = formLogin(request.POST or None)
    if request.POST:
        if frmLogin.is_valid():
            _email = frmLogin.cleaned_data.get('email') #captura o campo (nesse caso o email)
            _senha = frmLogin.cleaned_data.get('senha')
            try:
                usuario = Usuario.objects.get(email=_email, senha=_senha)
                if usuario is not None:
                    #SESSAO
                    request.session.set_expiry(timedelta(minutes=59))
                    request.session['email'] = _email

                    return redirect("dashboard")
            except Usuario.DoesNotExist:
                return render(request, "login.html")    
    return render(request, "login.html", {'form': frmLogin})

def dashboard(request):
    _email = request.session.get("email")
    if _email:
        try:
            usuario = Usuario.objects.get(email=_email)
            return render(request, "dashboard.html", {
                'usuario': usuario
            })
        except Usuario.DoesNotExist:
            messages.error(request, "Usuário não encontrado.")
            return redirect("login")
    else:
        messages.error(request, "Você precisa estar logado.")
        return redirect("login")




# CONSUMIR API
def consumirApi(request):
    resposta = requests.get("https://jsonplaceholder.typicode.com/users")
    dados = resposta.json()
    return render(request, 'api.html', {'response': dados})

# GRÁFICO
def grafico(request):
    produtos = Produto.objects.all().order_by('estoque')  # ordena pelo valor do estoque (ascendente)
    nome = [produto.nome for produto in produtos]
    estoque = [produto.estoque for produto in produtos]

    fig, ax = plt.subplots()
    ax.bar(nome, estoque, color='skyblue')  # cor opcional
    ax.set_xlabel("Produtos")
    ax.set_ylabel("Estoque")
    ax.set_title("Gráfico de Produtos")

    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    string = base64.b64encode(buf.read())
    uri = 'data:image/png;base64,' + urllib.parse.quote(string)

    return render(request, 'grafico.html', {'dados': uri})

# API: PRODUTOS
@api_view(['GET', 'POST'])
def getProdutos(request):
    if request.method == 'GET':
        produtos = Produto.objects.all()
        serializer = ProdutoSerializer(produtos, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProdutoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def getProdutoID(request, id_produto):
    try:
        produto = Produto.objects.get(id=id_produto)
    except Produto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProdutoSerializer(produto)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ProdutoSerializer(produto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        produto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#CEP 
def _buscar_endereco_por_cep(cep):
    url = f'https://viacep.com.br/ws/{cep}/json/'
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # dispara erro para status 4xx ou 5xx
        data = response.json()
        if 'erro' in data:
            return None
        return {
            'logradouro': data.get('logradouro', ''),
            'bairro': data.get('bairro', ''),
            'localidade': data.get('localidade', ''),
            'uf': data.get('uf', '')
        }
    except (requests.RequestException, ValueError):
        return None
    
    #CHECKOUT
def checkout(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)

    email = request.session.get("email")
    if not email:
        messages.error(request, "Sessão expirada. Faça login novamente.")
        return redirect("login")

    usuario = Usuario.objects.get(email=email)

    if request.method == 'POST':
        if int(produto.estoque) == 0:
            messages.error(request, "Produto fora de estoque. Não é possível realizar a compra.")
            return render(request, 'checkout.html', {'produto': produto, 'usuario': usuario})

        numero_cartao = request.POST.get('numero_cartao')
        validade = request.POST.get('validade')
        cvv = request.POST.get('cvv')

        Venda.objects.create(
            usuario=usuario,
            produto=produto,
            preço=produto.preço,
            numero_cartao=numero_cartao,
            validade=validade,
            cvv=cvv,
            data_compra=timezone.now()
        )
        # Atualiza o estoque
        produto.estoque = str(int(produto.estoque) - 1)
        produto.save()

        return render(request, 'confirmacao_compra.html', {'produto': produto})

    return render(request, 'checkout.html', {'produto': produto, 'usuario': usuario})


#GRAFICO DE VENDAS
def grafico_vendas(request):
    vendas_por_dia = (
        Venda.objects
        .annotate(data=TruncDate('data_compra'))
        .values('data')
        .annotate(total_vendas=Count('id'))
        .order_by('data')
    )

    datas = [v['data'].strftime('%d/%m/%Y') for v in vendas_por_dia]
    totais = [int(v['total_vendas']) for v in vendas_por_dia]

    fig, ax = plt.subplots()
    ax.plot(datas, totais, marker='o')
    ax.set_xlabel('Data')
    ax.set_ylabel('Total de Vendas')
    ax.set_title('Vendas por Dia')
    plt.xticks(rotation=45)

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)

    string = base64.b64encode(buf.read())
    uri = 'data:image/png;base64,' + urllib.parse.quote(string)

    return render(request, 'grafico_vendas.html', {'dados': uri})

#LOGOUT
def logout(request):
    request.session.flush()
    return redirect('login')