from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from .models import Livro

def lista_livros(request):
    query = request.GET.get('q')
    if query:
        livros = Livro.model_manager.filter(titulo__icontains=query) if hasattr(Livro, 'model_manager') else Livro.objects.filter(titulo__icontains=query)
    else:
        livros = Livro.objects.all()
    return render(request, 'livros/lista.html', {'livros': livros})

def adicionar_livro(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        autor = request.POST.get('autor')
        editora = request.POST.get('editora')
        ano_publicacao = request.POST.get('ano_publicacao')
        quantidade_exemplares = request.POST.get('quantidade_exemplares')
        disponivel = True if request.POST.get('disponivel') == 'on' else False

        Livro.objects.create(
            titulo=titulo,
            autor=autor,
            editora=editora,
            ano_publicacao=ano_publicacao,
            quantidade_exemplares=quantidade_exemplares,
            disponivel=disponivel
        )
        return redirect('lista_livros')
    return render(request, 'livros/form.html')

def editar_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    if request.method == 'POST':
        livro.titulo = request.POST.get('titulo')
        livro.autor = request.POST.get('autor')
        livro.editora = request.POST.get('editora')
        livro.ano_publicacao = request.POST.get('ano_publicacao')
        livro.quantidade_exemplares = request.POST.get('quantidade_exemplares')
        livro.disponivel = True if request.POST.get('disponivel') == 'on' else False
        livro.save()
        return redirect('lista_livros')
    return render(request, 'livros/form.html', {'livro': livro})

def excluir_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    if request.method == 'POST':
        livro.delete()
        return redirect('lista_livros')
    return render(request, 'livros/excluir.html', {'livro': livro})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Livro

def index(request):
    return render(request, 'livros/index.html')

def quem_somos(request):
    return render(request, 'livros/quem_somos.html')

def suporte(request):
    sucesso = False
    if request.method == 'POST':
        # Aqui você poderia salvar no banco ou enviar um e-mail futuramente
        sucesso = True
    return render(request, 'livros/suporte.html', {'sucesso': sucesso})

def lista_livros(request):
    query = request.GET.get('q')
    if query:
        livros = Livro.objects.filter(titulo__icontains=query)
    else:
        livros = Livro.objects.all()
    return render(request, 'livros/lista.html', {'livros': livros})

def adicionar_livro(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        autor = request.POST.get('autor')
        editora = request.POST.get('editora')
        ano_publicacao = request.POST.get('ano_publicacao')
        quantidade_exemplares = request.POST.get('quantidade_exemplares')
        disponivel = True if request.POST.get('disponivel') == 'on' else False

        Livro.objects.create(
            titulo=titulo,
            autor=autor,
            editora=editora,
            ano_publicacao=ano_publicacao,
            quantidade_exemplares=quantidade_exemplares,
            disponivel=disponivel
        )
        return redirect('lista_livros')
    return render(request, 'livros/form.html')

def editar_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    if request.method == 'POST':
        livro.titulo = request.POST.get('titulo')
        livro.autor = request.POST.get('autor')
        livro.editora = request.POST.get('editora')
        livro.ano_publicacao = request.POST.get('ano_publicacao')
        livro.quantidade_exemplares = request.POST.get('quantidade_exemplares')
        livro.disponivel = True if request.POST.get('disponivel') == 'on' else False
        livro.save()
        return redirect('lista_livros')
    return render(request, 'livros/form.html', {'livro': livro})

def excluir_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    if request.method == 'POST':
        livro.delete()
        return redirect('lista_livros')
    return render(request, 'livros/excluir.html', {'livro': livro})