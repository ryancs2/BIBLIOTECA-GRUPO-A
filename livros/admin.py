from django.contrib import admin
from .models import Livro, Pessoa, Emprestimo, MensagemSuporte

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'autor', 'editora', 'ano_publicacao', 'quantidade_exemplares', 'disponivel')
    search_fields = ('titulo', 'autor')
    list_filter = ('disponivel', 'ano_publicacao')


@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'nome_completo', 'cpf', 'rg', 'email', 'telefone', 'data_cadastro')
    search_fields = ('matricula', 'nome_completo', 'cpf', 'rg', 'email')
    readonly_fields = ('matricula', 'data_cadastro')

    fieldsets = (
        ('Identificação', {
            'fields': ('matricula', 'nome_completo', 'cpf', 'rg')
        }),
        ('Contato', {
            'fields': ('endereco', 'email', 'telefone')
        }),
        ('Sistema', {
            'fields': ('data_cadastro',)
        }),
    )


@admin.action(description='Marcar como devolvido')
def marcar_devolvido(modeladmin, request, queryset):
    for emprestimo in queryset.filter(devolvido=False):
        emprestimo.devolvido = True
        emprestimo.save()

        livro = emprestimo.livro
        livro.quantidade_exemplares += 1
        livro.disponivel = True
        livro.save()


@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ('id', 'livro', 'pessoa', 'data_emprestimo', 'devolvido')
    search_fields = ('pessoa__nome_completo', 'pessoa__cpf', 'pessoa__matricula', 'livro__titulo')
    list_filter = ('devolvido',)
    actions = [marcar_devolvido]
    autocomplete_fields = ('pessoa', 'livro')
    readonly_fields = ('data_emprestimo',)

    fieldsets = (
        ('Livro', {
            'fields': ('livro',)
        }),
        ('Solicitante', {
            'fields': ('pessoa',)
        }),
        ('Detalhes', {
            'fields': ('observacao', 'data_emprestimo', 'devolvido')
        }),
    )


@admin.register(MensagemSuporte)
class MensagemSuporteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email', 'data_envio')
    search_fields = ('nome', 'email')
    readonly_fields = ('data_envio',)