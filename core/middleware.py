class ThemeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Set theme from session or default to dark
        if 'theme' not in request.session:
            request.session['theme'] = 'dark'
            
        response = self.get_response(request)
        return response