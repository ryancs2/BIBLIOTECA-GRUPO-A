from django.db import models


class Livro(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título", db_index=True)
    autor = models.CharField(max_length=150, verbose_name="Autor")
    editora = models.CharField(max_length=100, verbose_name="Editora")
    ano_publicacao = models.IntegerField(verbose_name="Ano de Publicação")
    quantidade_exemplares = models.IntegerField(verbose_name="Quantidade de Exemplares")
    disponivel = models.BooleanField(default=True, verbose_name="Disponível")

    class Meta:
        ordering = ['titulo']
        indexes = [
            models.Index(fields=['disponivel']),
        ]

    def __str__(self):
        return f"{self.titulo} - {self.autor}"


class Emprestimo(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, verbose_name="Livro", related_name='emprestimos')
    nome_completo = models.CharField(max_length=150, verbose_name="Nome Completo")
    cpf = models.CharField(max_length=14, verbose_name="CPF", db_index=True, blank=True)
    rg = models.CharField(max_length=20, verbose_name="RG", db_index=True, blank=True)
    endereco = models.CharField(max_length=255, verbose_name="Endereço")
    email = models.EmailField(verbose_name="E-mail")
    telefone = models.CharField(max_length=20, verbose_name="Telefone de Contato")
    observacao = models.TextField(blank=True, null=True, verbose_name="Observação")
    data_emprestimo = models.DateField(auto_now_add=True, verbose_name="Data da Solicitação")
    devolvido = models.BooleanField(default=False, verbose_name="Devolvido")

    class Meta:
        ordering = ['-data_emprestimo']
        indexes = [
            models.Index(fields=['cpf', 'devolvido']),
            models.Index(fields=['rg', 'devolvido']),
        ]

    def __str__(self):
        return f"Empréstimo de {self.livro.titulo} para {self.nome_completo}"