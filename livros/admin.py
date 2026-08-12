from django.contrib import admin
from .models import Livro, Emprestimo, MensagemSuporte

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'autor', 'editora', 'ano_publicacao', 'quantidade_exemplares', 'disponivel')
    search_fields = ('titulo', 'autor')
    list_filter = ('disponivel', 'ano_publicacao')

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
    list_display = ('id', 'livro', 'nome_completo', 'cpf', 'data_emprestimo', 'devolvido')
    search_fields = ('nome_completo', 'cpf')
    list_filter = ('devolvido',)
    actions = [marcar_devolvido]

@admin.register(MensagemSuporte)
class MensagemSuporteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email', 'data_envio', 'mensagem_resumida')
    search_fields = ('nome', 'email')

    def mensagem_resumida(self, obj):
        return obj.mensagem[:300] + '...' if len(obj.mensagem) > 300 else obj.mensagem
    mensagem_resumida.short_description = 'Mensagem'