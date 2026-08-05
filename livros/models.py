from django.db import models

# Create your models here.

from django.db import models

class Livro(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título")
    autor = models.CharField(max_length=150, verbose_name="Autor")
    editora = models.CharField(max_length=100, verbose_name="Editora")
    ano_publicacao = models.IntegerField(verbose_name="Ano de Publicação")
    quantidade_exemplares = models.IntegerField(verbose_name="Quantidade de Exemplares")
    disponivel = models.BooleanField(default=True, verbose_name="Disponível")

    def __str__(self):
        return f"{self.titulo} - {self.autor}"