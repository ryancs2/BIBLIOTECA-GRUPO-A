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


class Pessoa(models.Model):
    matricula = models.CharField(max_length=20, unique=True, editable=False, verbose_name="Matrícula")
    nome_completo = models.CharField(max_length=150, verbose_name="Nome Completo")
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    rg = models.CharField(max_length=20, unique=True, verbose_name="RG")
    endereco = models.CharField(max_length=255, verbose_name="Endereço")
    email = models.EmailField(verbose_name="E-mail")
    telefone = models.CharField(max_length=20, verbose_name="Telefone de Contato")
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")

    class Meta:
        verbose_name = "Pessoa"
        verbose_name_plural = "Pessoas"

    def save(self, *args, **kwargs):
        if not self.matricula:
            ultima = Pessoa.objects.order_by('-id').first()
            proximo_numero = (ultima.id + 1) if ultima else 1
            self.matricula = f"MAT{proximo_numero:06d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome_completo} ({self.matricula})"


class Emprestimo(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, verbose_name="Livro")
    pessoa = models.ForeignKey(Pessoa, on_delete=models.PROTECT, verbose_name="Pessoa", related_name="emprestimos")
    observacao = models.TextField(blank=True, null=True, verbose_name="Observação")
    data_emprestimo = models.DateField(auto_now_add=True, verbose_name="Data da Solicitação")
    devolvido = models.BooleanField(default=False, verbose_name="Devolvido")

    def __str__(self):
        return f"Empréstimo de {self.livro.titulo} para {self.pessoa.nome_completo}"


class MensagemSuporte(models.Model):
    nome = models.CharField(max_length=150, verbose_name="Nome")
    email = models.EmailField(verbose_name="E-mail")
    mensagem = models.TextField(verbose_name="Mensagem")
    data_envio = models.DateTimeField(auto_now_add=True, verbose_name="Data de Envio")

    def __str__(self):
        return f"{self.nome} - {self.data_envio.strftime('%d/%m/%Y')}"