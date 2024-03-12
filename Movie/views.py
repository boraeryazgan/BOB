from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm, SignUpForm
from django.core.paginator import Paginator
from .models import TVSeries
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse
from django.template import loader

@ensure_csrf_cookie
def search(request):
    query = request.POST.get('q', '')

    if query:
        series = TVSeries.objects.filter(series_title__icontains=query)  
        context = {'query': query, 'series': series}
        template = loader.get_template('movie_app/search.html')
        return HttpResponse(template.render(context, request))
    else:
        return render(request, 'movie_app/search.html')
    
def detail(request, serie_id):
    serie = TVSeries.objects.get(pk=serie_id)
    return render(request, 'movie_app/detail.html', {'serie': serie})

def index(request):
    series_list = TVSeries.objects.all()
    paginator = Paginator(series_list, 20) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'movie_app/index.html', {'page_obj': page_obj})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')  
            else:
                messages.error(request, 'Kullanıcı adı veya şifre yanlış.')
    else:
        form = LoginForm()
    return render(request, 'movie_app/login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():  
            user = form.save(commit=False)  
            user.is_active = True  
            user.save()  
            login(request, user)
            return redirect('/') 
        else:
            if 'username' in form.errors:
                messages.error(request, 'Bu kullanıcı adı zaten kullanılıyor. Lütfen farklı bir kullanıcı adı seçin.')
            
            if 'email' in form.errors:
                messages.error(request, 'Bu e-posta adresi zaten kullanılıyor. Lütfen farklı bir e-posta adresi seçin.')

            if 'password1' in form.errors or 'password2' in form.errors:
                messages.error(request, 'Girdiğiniz şifreler eşleşmiyor veya şifre yeterliliklerini karşılamıyor. Lütfen şifrenizi kontrol edin.')

            if 'username' not in form.data:
                messages.error(request, 'Kullanıcı adı alanı boş bırakılamaz.')
            
            if 'email' not in form.data:
                messages.error(request, 'E-posta alanı boş bırakılamaz.')
            
            return render(request, 'movie_app/signup.html')
 
    else:
        form = SignUpForm()
    return render(request, 'movie_app/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/') 
