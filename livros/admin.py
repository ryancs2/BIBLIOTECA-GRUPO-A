from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Livro

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'autor', 'editora', 'ano_publicacao', 'quantidade_exemplares', 'disponivel')
    search_fields = ('titulo', 'autor')
    list_filter = ('disponivel', 'ano_publicacao')