from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('quem-somos/', views.quem_somos, name='quem_somos'),
    path('suporte/', views.suporte, name='suporte'),
    path('acervo/', views.lista_livros, name='lista_livros'),
    path('emprestimo/', views.solicitar_emprestimo, name='solicitar_emprestimo'),
    path('historico/', views.historico_usuario, name='historico_usuario'),
    path('buscar-api/', views.buscar_livro_api, name='buscar_livro_api'),
    path('cadastrar-via-api/', views.cadastrar_via_api, name='cadastrar_via_api'),
    path('devolver/<int:emprestimo_id>/', views.devolver_livro, name='devolver_livro'),
]