"""
URL configuration for clique_seguro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    
    # Autenticação
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'), # <-- ADICIONADO: Rota para sair da conta
    path('registro/', register_view, name='register'),
    
    # Categorias e Tutoriais
    path('categoria/<str:category_id>/', category_page, name='category'),
    path('categoria/<str:category_id>/<str:tutorial_id>/', tutorial_page, name='tutorial'),
    
    # Dicionário
    path('dicionario/', dictionary_menu, name='dictionary_menu'),
    path('dicionario/icones/', dictionary_icons, name='dictionary_icons'),
    path('dicionario/palavras/', dictionary_words, name='dictionary_words'),
    
    # Perfil e Progresso
    path('perfil/', user_progress_view, name='user_progress'),
    path('concluir/<str:tutorial_id>/', concluir_tutorial, name='concluir_tutorial'), # <-- ADICIONADO: Rota para registar progresso
    path('alternar-contraste/', toggle_contrast, name='toggle_contrast'),
]