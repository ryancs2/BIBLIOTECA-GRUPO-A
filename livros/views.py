from django.shortcuts import render, redirect, get_object_or_404
from .models import Livro, Emprestimo

def index(request):
    return render(request, 'livros/index.html')

def quem_somos(request):
    return render(request, 'livros/quem_somos.html')

def suporte(request):
    sucesso = False
    if request.method == 'POST':
        sucesso = True
    return render(request, 'livros/suporte.html', {'sucesso': sucesso})

def lista_livros(request):
    query = request.GET.get('q')
    if query:
        livros = Livro.objects.filter(titulo__icontains=query)
    else:
        livros = Livro.objects.all()
    return render(request, 'livros/lista.html', {'livros': livros})

def solicitar_emprestimo(request):
    livros_disponiveis = Livro.objects.filter(disponivel=True, quantidade_exemplares__gt=0)
    erro = None
    
    if request.method == 'POST':
        nome_solicitante = request.POST.get('nome_solicitante')
        livro_id = request.POST.get('livro_id')
        
        livro = get_object_or_404(Livro, id=livro_id)
        
        if livro.quantidade_exemplares > 0 and livro.disponivel:
            # Cria o registro do empréstimo
            Emprestimo.objects.create(livro=livro, nome_solicitante=nome_solicitante)
            # Atualiza a quantidade e disponibilidade
            livro.quantidade_exemplares -= 1
            if livro.quantidade_exemplares == 0:
                livro.disponivel = False
            livro.save()
            return redirect('lista_livros')
        else:
            erro = "Desculpe, este livro não está disponível no momento."
            
    return render(request, 'livros/emprestimo_form.html', {
        'livros_disponiveis': livros_disponiveis,
        'erro': erro
    })