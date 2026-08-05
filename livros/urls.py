from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('quem-somos/', views.quem_somos, name='quem_somos'),
    path('suporte/', views.suporte, name='suporte'),
    path('acervo/', views.lista_livros, name='lista_livros'),
    path('novo/', views.adicionar_livro, name='adicionar_livro'),
    path('editar/<int:pk>/', views.editar_livro, name='editar_livro'),
    path('excluir/<int:pk>/', views.excluir_livro, name='excluir_livro'),
]