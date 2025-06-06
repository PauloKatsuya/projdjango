from django.urls import path

from . import views

urlpatterns = [
    path('', views.app, name="app"),
    path('usuarios', views.exibirUsuarios, name="exibirUsuarios"),
    path('produtos', views.exibirProdutos, name="exibirProdutos"), # digitar usuarios para entrar na página na url
    path('add-usuario', views.addUsuario, name="addUsuario"),
    path('add-produtos', views.addProduto, name="addProduto"),
    # rota que vai apárecer na url, view, nome
    
    #Excluir usuario
    path('excluir-usuario/<int:id_usuario>', views.excluirUsuario, name="excluirUsuario"),

    #Editar USuario
    path('editar-usuario/<int:id_usuario>', views.editarUsuario, name="editarUsuario"),

    #Excluir produto
    path('excluir-produto/<int:id_produtos>', views.excluirProduto, name="excluirProduto"),

    #Editar produto
    path('editar-produto/<int:id_produtos>', views.editarProduto, name="editarProduto"),

    path('login', views.login, name="login"),

    path('logout/', views.logout, name='logout'),

    path('dashboard', views.dashboard, name="dashboard"),
    
    path('checkout/<int:produto_id>/', views.checkout, name='checkout'),

    path('consumir_api/', views.consumirApi, name='consumir_api'),

    path('grafico', views.grafico, name="grafico"),

    #URL APP: API (pra seguir o esquema do serializer)
    # Gráfico
    path('grafico/', views.grafico, name='grafico'),
    path('grafico_vendas/', views.grafico_vendas, name='grafico_vendas'),

    # API REST
    path('api/produtos/', views.getProdutos, name='getProdutos'),
    path('api/produtos/<int:id_produto>/', views.getProdutoID, name='getProdutoID'),
]