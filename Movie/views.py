from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm, SignUpForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import TVSeries, Review, Playlist
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse
from django.template import loader
from django.db.models.functions import Length

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
    serie = get_object_or_404(TVSeries, pk=serie_id)
    review = Review.objects.filter(tv_serie=serie_id)
    similar_series = TVSeries.objects.filter(genre=serie.genre).exclude(pk=serie_id)
    similar_series = similar_series.order_by('-imdb_rating')
    if similar_series.count() >= 5:
        similar_series = list(similar_series[:5])
    elif 1 < similar_series.count() < 5:
        similar_series = list(similar_series)
    else:
        similar_series = []

    liked_playlist = Playlist.objects.filter(user=request.user,is_like_playlist=True)
    if len(liked_playlist) != 0:
        liked_playlist = liked_playlist[0]
        is_associated = Playlist.objects.filter(movies=serie).exists()
        if is_associated:
            like_button_statement = False
        else:
            like_button_statement = True
    else:
        like_button_statement = True
    return render(request, 'movie_app/detail.html', {'serie': serie, 'similar_series': similar_series,"reviews":review,"like_button_statement":like_button_statement})

def index(request):
    series_list = TVSeries.objects.all()

    order_by = request.GET.get('sorting', 'default')

    if order_by == 'released_year-ascending':
        series_list = series_list.order_by('released_year')
    elif order_by == 'released_year-descending':
        series_list = series_list.order_by('-released_year')
    elif order_by == 'runtime-ascending':
        series_list = series_list.annotate(runtime_length=Length('runtime')).order_by('runtime_length', 'runtime')
    elif order_by == 'runtime-descending':
        series_list = series_list.annotate(runtime_length=Length('runtime')).order_by('-runtime_length', '-runtime')
    elif order_by == 'imdb_rating-ascending':
        series_list = series_list.order_by('imdb_rating')
    elif order_by == 'imdb_rating-descending':
        series_list = series_list.order_by('-imdb_rating')
    elif order_by == 'no_of_votes-ascending':
        series_list = series_list.order_by('no_of_votes')
    elif order_by == 'no_of_votes-descending':
        series_list = series_list.order_by('-no_of_votes')

    paginator = Paginator(series_list, 20)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    current_url = request.build_absolute_uri()

    url_parts = current_url.split('?')
    base_url = url_parts[0]
    query_params = url_parts[1].split('&') if len(url_parts) > 1 else []
    filtered_params = [param for param in query_params if 'page=' not in param]
    current_url = base_url + '?' + '&'.join(filtered_params)

    current_url += f'&page={page_number}'

    return render(request, 'movie_app/index.html', {'page_obj': page_obj, 'order_by': order_by, 'current_url': current_url})

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

def review_rate(request):
    if request.method == "GET":
        serie_id = request.GET.get("serie_id")
        serie = TVSeries.objects.get(id=serie_id)
        comment = request.GET.get("comment")
        rate = request.GET.get("rating")
        user = request.user
        Review(user=user, tv_serie=serie, comment=comment, rate=rate).save()
        return redirect("detail",serie_id=serie_id)

def add_to_liked_list(request):
    if request.method == "GET":
        if request.GET.get("like",None) == "True":
            # Liked movies list
            serie_id = request.GET.get("serie_id")
            serie = TVSeries.objects.get(id=serie_id)
            user = request.user
            title_str = f"Liked films of {user.username}"
            liked_movies_playlist = Playlist.objects.filter(user=user,is_like_playlist=True)
            if len(liked_movies_playlist) == 0:
                # Create playlist
                q = Playlist.objects.create(title=title_str, user=user, is_like_playlist=True)
                q.movies.add(serie)
            else:
                q = Playlist.objects.filter(user=user,is_like_playlist=True)[0]
                q.movies.add(serie)
        if request.GET.get("playlist",None) == "True":
            # Other playlist
            pass
        return redirect("detail",serie_id=serie_id)

