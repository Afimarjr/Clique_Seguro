def contrast_processor(request):
    """
    Verifica na sessão do utilizador se o alto contraste está ativado.
    Envia a variável 'high_contrast' automaticamente para todos os HTMLs.
    """
    return {
        'high_contrast': request.session.get('high_contrast', False)
    }