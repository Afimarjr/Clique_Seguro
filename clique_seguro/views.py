from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from main.models import Categoria, Tutorial, Passo, Progresso
from django.contrib.auth.models import User

# ==========================================
# 1. PÁGINAS PRINCIPAIS E AUTENTICAÇÃO
# ==========================================

def home_view(request):
    """Renderiza a página inicial (Homepage)."""
    context = {
        'is_logged_in': request.user.is_authenticated,
        'username': request.user.username if request.user.is_authenticated else ''
    }
    return render(request, 'homepage.html', context)

def login_view(request):
    """Processa o Login usando E-mail."""
    if request.method == 'POST':
        email = request.POST.get('email') # Agora recebemos o e-mail
        senha = request.POST.get('password')
        
        # Como guardamos o e-mail no campo username no registo, verificamos assim:
        user = authenticate(request, username=email, password=senha)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {
                'error': 'E-mail ou senha incorretos.',
                'old_email': email
            })
            
    return render(request, 'login.html')

def logout_view(request):
    """Faz o logout do utilizador."""
    logout(request)
    return redirect('home')

# Não se esqueça de garantir que o User está importado lá no topo do ficheiro:
# from django.contrib.auth.models import User

def register_view(request):
    """Processa o Registo pedindo Nome e E-mail."""
    if request.method == 'POST':
        nome = request.POST.get('first_name')
        email = request.POST.get('email')
        senha = request.POST.get('password')
        confirmar_senha = request.POST.get('confirm_password')
        
        # 1. Verificar senhas
        if senha != confirmar_senha:
            return render(request, 'register.html', {
                'error': 'As senhas não são iguais. Por favor, digite com calma e tente de novo.',
                'old_name': nome,
                'old_email': email
            })
            
        # 2. Verificar se o E-mail já existe
        if User.objects.filter(username=email).exists():
            return render(request, 'register.html', {
                'error': 'Este e-mail já está registado. Se já tem conta, clique em "Entrar".',
                'old_name': nome
            })
            
        # 3. Criar conta (Guardamos o email como 'username' e o nome como 'first_name')
        user = User.objects.create_user(
            username=email, 
            email=email, 
            password=senha, 
            first_name=nome
        )
        login(request, user)
        return redirect('home')
        
    return render(request, 'register.html')


# ==========================================
# 2. CATEGORIAS E TUTORIAIS (USANDO BANCO DE DADOS)
# ==========================================

def category_page(request, category_id):
    """Renderiza a página de uma Categoria específica com a sua lista de tutoriais."""
    category = Categoria.objects.filter(id=category_id).first()
    
    if not category:
        return redirect('home')

    # Busca os tutoriais associados a esta categoria no Banco de Dados
    tutorials = category.tutorials.all()

    context = {
        'category': category,
        'tutorials': tutorials
    }
    return render(request, 'category_page.html', context)

def tutorial_page(request, category_id, tutorial_id):
    """Renderiza os passos de um tutorial específico."""
    category = Categoria.objects.filter(id=category_id).first()
    if not category:
        return redirect('home')
        
    tutorial = Tutorial.objects.filter(id=tutorial_id, categoria=category).first()
    if not tutorial:
        return redirect('category', category_id=category_id)
        
    # Busca os passos ordenados do Banco de Dados
    steps = tutorial.steps.all().order_by('ordem')
    
    context = {
        'category': category,
        'tutorial': tutorial,
        'steps': steps
    }
    return render(request, 'tutorial_page.html', context)


# ==========================================
# 3. REGISTO DE PROGRESSO E PERFIL
# ==========================================

@login_required # Garante que apenas pessoas logadas possam concluir tutoriais
def concluir_tutorial(request, tutorial_id):
    """Regista no banco de dados que o utilizador concluiu um tutorial."""
    if request.method == 'POST':
        tutorial = Tutorial.objects.filter(id=tutorial_id).first()
        
        if tutorial:
            # Cria o registo de conclusão. Se já existir, não faz nada (evita duplicados)
            Progresso.objects.get_or_create(
                usuario=request.user,
                tutorial=tutorial
            )
            return JsonResponse({'success': True, 'message': 'Progresso salvo!'})
            
    return JsonResponse({'success': False, 'message': 'Erro ao salvar.'}, status=400)


@login_required # Garante que a pessoa tem de estar logada para ver o perfil
def user_progress_view(request):
    """Processa e renderiza as estatísticas do perfil do utilizador."""
    
    # 1. Busca todos os progressos deste utilizador, do mais recente para o mais antigo
    progressos = Progresso.objects.filter(usuario=request.user).order_by('-concluido_em')
    total_completed = progressos.count()
    
    # 2. Busca os nomes dos 5 últimos tutoriais concluídos
    recent_completions = [p.tutorial.title for p in progressos[:5]]
    
    # 3. Total de tutoriais no sistema
    total_tutorials = Tutorial.objects.count()
    progress_percentage = round((total_completed / total_tutorials) * 100) if total_tutorials > 0 else 0
    
    # 4. Cálculos detalhados por categoria
    categories = []
    for cat in Categoria.objects.all():
        total_na_cat = cat.tutorials.count()
        completados_na_cat = progressos.filter(tutorial__categoria=cat).count()
        percent = round((completados_na_cat / total_na_cat) * 100) if total_na_cat > 0 else 0
        
        categories.append({
            'name': cat.name,
            'completed': completados_na_cat,
            'total': total_na_cat,
            'percentage': percent,
            'color_class': cat.color
        })

    context = {
        'username': request.user.username,
        'total_tutorials': total_tutorials,
        'completed_tutorials': total_completed,
        'progress_percentage': progress_percentage,
        'categories': categories,
        'recent_completions': recent_completions
    }
    return render(request, 'user_progress.html', context)


# ==========================================
# 4. DICIONÁRIO E ACESSIBILIDADE
# ==========================================

def dictionary_menu(request):
    """Renderiza o menu principal do dicionário."""
    return render(request, 'dictionary_menu.html')

def dictionary_icons(request):
    """Renderiza o dicionário de ícones."""
    icon_categories = [
        {
            'name': 'Comunicação Básica',
            'icons': [
                {
                    'name': 'Telefone Verde',
                    'meaning': 'Serve para atender uma chamada ou iniciar uma nova ligação.',
                    'svg': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="w-full h-full"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
                }
            ]
        }
    ]
    return render(request, 'dictionary_icons.html', {'icon_categories': icon_categories})

def dictionary_words(request):
    """Renderiza o dicionário de palavras."""
    words_data = [
        {
            'word': 'App (Aplicação)',
            'definition': 'Um programa que instala no telemóvel para fazer algo específico.',
            'example': 'Exemplo: "Vou descarregar a app do banco para ver o saldo."'
        },
        {
            'word': 'Wi-Fi',
            'definition': 'Internet sem fios. Permite que o telemóvel se ligue à internet sem gastar dados móveis.',
            'example': 'Exemplo: "Estou ligado ao Wi-Fi de casa."'
        }
    ]
    return render(request, 'dictionary_words.html', {'words': words_data})

def toggle_contrast(request):
    """Liga e desliga o modo de Alto Contraste na sessão."""
    request.session['high_contrast'] = not request.session.get('high_contrast', False)
    return redirect(request.META.get('HTTP_REFERER', 'home'))