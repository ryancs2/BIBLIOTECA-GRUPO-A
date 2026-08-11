from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.db.models import Q
from django.views.decorators.cache import cache_page
from .models import Livro, Emprestimo


@cache_page(60 * 60)
def index(request):
    return render(request, 'livros/index.html')


@cache_page(60 * 60)
def quem_somos(request):
    return render(request, 'livros/quem_somos.html')


def suporte(request):
    sucesso = False
    if request.method == 'POST':
        sucesso = True
    return render(request, 'livros/suporte.html', {'sucesso': sucesso})


def lista_livros(request):
    from django.core.paginator import Paginator

    query = request.GET.get('q')
    livros_qs = Livro.objects.only(
        'titulo', 'autor', 'editora', 'ano_publicacao',
        'quantidade_exemplares', 'disponivel'
    )

    if query:
        livros_qs = livros_qs.filter(titulo__icontains=query)

    paginator = Paginator(livros_qs, 20)
    page_number = request.GET.get('page')
    livros = paginator.get_page(page_number)

    return render(request, 'livros/lista.html', {
        'livros': livros,
        'query': query or '',
    })


def solicitar_emprestimo(request):
    livros_disponiveis = Livro.objects.filter(
        disponivel=True, quantidade_exemplares__gt=0
    ).only('id', 'titulo', 'quantidade_exemplares')
    erro = None

    if request.method == 'POST':
        cpf = (request.POST.get('cpf') or '').strip()
        rg = (request.POST.get('rg') or '').strip()

        if not cpf and not rg:
            erro = "Informe pelo menos o CPF ou o RG."
            return render(request, 'livros/emprestimo_form.html', {
                'livros_disponiveis': livros_disponiveis,
                'erro': erro
            })

        livro_id = request.POST.get('livro_id')

        with transaction.atomic():
            livro = get_object_or_404(
                Livro.objects.select_for_update(),
                id=livro_id, disponivel=True, quantidade_exemplares__gt=0
            )

            Emprestimo.objects.create(
                livro=livro,
                nome_completo=request.POST.get('nome_completo'),
                cpf=cpf,
                rg=rg,
                endereco=request.POST.get('endereco'),
                email=request.POST.get('email'),
                telefone=request.POST.get('telefone'),
                observacao=request.POST.get('observacao')
            )

            livro.quantidade_exemplares -= 1
            if livro.quantidade_exemplares == 0:
                livro.disponivel = False
            livro.save(update_fields=['quantidade_exemplares', 'disponivel'])

        return redirect('lista_livros')

    return render(request, 'livros/emprestimo_form.html', {
        'livros_disponiveis': livros_disponiveis,
        'erro': erro
    })


def historico_usuario(request):
    documento = request.GET.get('documento', '').strip()
    emprestimos_ativos = []
    emprestimos_devolvidos = []

    if documento:
        base_qs = Emprestimo.objects.filter(
            Q(cpf=documento) | Q(rg=documento)
        ).select_related('livro').only(
            'data_emprestimo', 'livro__titulo', 'livro__autor', 'cpf', 'rg', 'devolvido'
        )
        emprestimos_ativos = base_qs.filter(devolvido=False)
        emprestimos_devolvidos = base_qs.filter(devolvido=True)

    return render(request, 'livros/historico.html', {
        'emprestimos_ativos': emprestimos_ativos,
        'emprestimos_devolvidos': emprestimos_devolvidos,
        'documento': documento
    })