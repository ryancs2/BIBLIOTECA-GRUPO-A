from django.contrib import admin
from .models import Livro, Emprestimo, MensagemSuporte

# Register your models here.

from django.contrib import admin
from .models import Livro

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'autor', 'editora', 'ano_publicacao', 'quantidade_exemplares', 'disponivel')
    search_fields = ('titulo', 'autor')
    list_filter = ('disponivel', 'ano_publicacao')

@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ('id', 'livro', 'nome_completo', 'cpf', 'data_emprestimo', 'devolvido')
    search_fields = ('nome_completo', 'cpf')
    list_filter = ('devolvido',)

@admin.register(MensagemSuporte)
class MensagemSuporteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email', 'data_envio')
    search_fields = ('nome', 'email')