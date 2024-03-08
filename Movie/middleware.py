from django.shortcuts import redirect
from django.urls import reverse

class AuthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            
            if request.path in [reverse('signup'), reverse('login')]:
                return redirect('/')
        return self.get_response(request)
