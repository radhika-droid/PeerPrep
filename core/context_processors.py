def theme_context(request):
    """Add theme information to all templates"""
    return {
        'current_theme': request.session.get('theme', 'dark'),
    }