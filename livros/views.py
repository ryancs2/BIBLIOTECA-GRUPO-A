from django.shortcuts import render, redirect, get_object_or_404
from .models import Livro, Pessoa, Emprestimo, MensagemSuporte
import requests
from django.contrib import messages

def index(request):
    return render(request, 'livros/index.html')

def quem_somos(request):
    return render(request, 'livros/quem_somos.html')

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
        livro_id = request.POST.get('livro_id')
        livro = get_object_or_404(Livro, id=livro_id)
        
        if livro.quantidade_exemplares > 0 and livro.disponivel:
            cpf = request.POST.get('cpf')
            rg = request.POST.get('rg')
            nome_completo = request.POST.get('nome_completo')

            pessoa_existente = Pessoa.objects.filter(cpf=cpf).first()

            if pessoa_existente:
                if pessoa_existente.rg != rg or pessoa_existente.nome_completo != nome_completo:
                    erro = "Este CPF já está cadastrado com outros dados (nome ou RG divergentes). Verifique as informações."
                    return render(request, 'livros/emprestimo_form.html', {
                        'livros_disponiveis': livros_disponiveis,
                        'erro': erro
                    })
                pessoa = pessoa_existente
            else:
                if Pessoa.objects.filter(rg=rg).exists():
                    erro = "Este RG já está cadastrado para outro CPF. Verifique as informações."
                    return render(request, 'livros/emprestimo_form.html', {
                        'livros_disponiveis': livros_disponiveis,
                        'erro': erro
                    })

                pessoa = Pessoa.objects.create(
                    cpf=cpf,
                    rg=rg,
                    nome_completo=nome_completo,
                    endereco=request.POST.get('endereco'),
                    email=request.POST.get('email'),
                    telefone=request.POST.get('telefone'),
                )

            Emprestimo.objects.create(
                livro=livro,
                pessoa=pessoa,
                observacao=request.POST.get('observacao')
            )
            
            livro.quantidade_exemplares -= 1
            if livro.quantidade_exemplares == 0:
                livro.disponivel = False
            livro.save()

            messages.success(
                request,
                f"Empréstimo solicitado com sucesso! Sua matrícula é: {pessoa.matricula}. Guarde este número para futuras consultas."
            )
            return redirect('lista_livros')
        else:
            erro = "Desculpe, este livro não está disponível no momento."
            
    return render(request, 'livros/emprestimo_form.html', {
        'livros_disponiveis': livros_disponiveis,
        'erro': erro
    })

def historico_usuario(request):
    busca = request.GET.get('busca', '').strip()
    emprestimos_ativos = []
    emprestimos_devolvidos = []
    pessoa = None
    erro = None

    if busca:
        pessoa = Pessoa.objects.filter(matricula__iexact=busca).first() or \
                 Pessoa.objects.filter(cpf=busca).first()

        if pessoa:
            emprestimos_ativos = Emprestimo.objects.filter(pessoa=pessoa, devolvido=False)
            emprestimos_devolvidos = Emprestimo.objects.filter(pessoa=pessoa, devolvido=True)
        else:
            erro = "Nenhum cadastro encontrado com o CPF ou matrícula informado."

    return render(request, 'livros/historico.html', {
        'emprestimos_ativos': emprestimos_ativos,
        'emprestimos_devolvidos': emprestimos_devolvidos,
        'pessoa': pessoa,
        'busca': busca,
        'erro': erro,
    })

def buscar_livro_api(request):
    resultados = []
    query = request.GET.get('q')

    if query:
        url = f"https://openlibrary.org/search.json?q={query}&limit=12"
    else:
        url = "https://openlibrary.org/search.json?q=subject:fiction&sort=random&limit=12"

    resp = requests.get(url).json()
    for item in resp.get('docs', []):
        capa_id = item.get('cover_i')
        resultados.append({
            'titulo': item.get('title', ''),
            'autor': ', '.join(item.get('author_name', [])),
            'editora': ', '.join(item.get('publisher', [])[:1]) if item.get('publisher') else '',
            'ano': item.get('first_publish_year', ''),
            'capa': f"https://covers.openlibrary.org/b/id/{capa_id}-M.jpg" if capa_id else '',
        })
    return render(request, 'livros/buscar_api.html', {'resultados': resultados, 'query': query})

def cadastrar_via_api(request):
    if request.method == 'POST':
        Livro.objects.create(
            titulo=request.POST.get('titulo'),
            autor=request.POST.get('autor') or 'Desconhecido',
            editora=request.POST.get('editora') or 'Desconhecida',
            ano_publicacao=request.POST.get('ano') or 0,
            quantidade_exemplares=1,
            disponivel=True
        )
        return redirect('lista_livros')
    return redirect('buscar_livro_api')

def suporte(request):
    sucesso = False
    if request.method == 'POST':
        MensagemSuporte.objects.create(
            nome=request.POST.get('nome'),
            email=request.POST.get('email'),
            mensagem=request.POST.get('mensagem')
        )
        sucesso = True
    return render(request, 'livros/suporte.html', {'sucesso': sucesso})

def devolver_livro(request, emprestimo_id):
    emprestimo = get_object_or_404(Emprestimo, id=emprestimo_id, devolvido=False)

    if request.method == 'POST':
        emprestimo.devolvido = True
        emprestimo.save()

        livro = emprestimo.livro
        livro.quantidade_exemplares += 1
        livro.disponivel = True
        livro.save()

        return redirect('historico_usuario')

    return render(request, 'livros/devolver.html', {'emprestimo': emprestimo})