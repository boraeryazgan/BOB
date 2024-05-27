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
from django.contrib.auth.decorators import login_required
from django.db.models import F,Q

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

    like_button_statement = None
    if request.user.is_authenticated:
        if Playlist.objects.filter(user=request.user, is_like_playlist=True).exists(): # If playlist exists
            liked_playlist = Playlist.objects.filter(user=request.user, is_like_playlist=True)[0]
            if serie in liked_playlist.movies.all():
                like_button_statement = False
            else:
                like_button_statement = True
        else:
            like_button_statement = True

        user_playlists = Playlist.objects.filter(user=request.user,is_like_playlist=False)

    return render(request, 'movie_app/detail.html', {'serie': serie, 'similar_series': similar_series,"reviews":review,"like_button_statement":like_button_statement,
                                                     "user_playlists":user_playlists})

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
    if request.method == "GET" and request.GET.get("like",None) == "True":
        # Liked movies list
        serie_id = request.GET.get("serie_id")
        serie = TVSeries.objects.get(id=serie_id)
        user = request.user
        title_str = f"Liked films of {user.username}"

        if Playlist.objects.filter(user=user,is_like_playlist=True).exists(): #If user has liked movies playlist
            users_liked_playlist = Playlist.objects.filter(user=user,is_like_playlist=True)[0]
            if serie in users_liked_playlist.movies.all(): # Check if movie is in the playlist
                users_liked_playlist.movies.remove(serie)
            else:
                users_liked_playlist.movies.add(serie)
        else: # If user does not have liked movies playlist
            q = Playlist.objects.create(title=title_str, user=user, is_like_playlist=True)
            q.movies.add(serie)

        return redirect("detail",serie_id=serie_id)

def add_to_playlist(request):
    serie_id = request.GET.get("serie_id")
    serie = TVSeries.objects.get(id=serie_id)
    user = request.user
    print(request.GET)
    print(bool(request.GET["newPlaylistName"]))
    if request.method == "GET":
        if request.GET.get("playlist",None) == "True": # Create playlist button
            if request.GET.get("newPlaylistName", None):
                new_playlist_name = request.GET["newPlaylistName"]
                q = Playlist.objects.create(title=new_playlist_name, user=user, is_like_playlist=False)
                q.movies.add(serie)


        elif request.GET.get("RemovePlaylistButton",None):
            q = Playlist.objects.filter(id=request.GET["RemovePlaylistButton"])[0]
            q.movies.remove(serie)

        elif request.GET.get("AddPlaylistButton",None):
            q = Playlist.objects.filter(id=request.GET["AddPlaylistButton"])[0]
            q.movies.add(serie)


    return redirect("detail",serie_id=serie_id)

@login_required
def recommend_similar_series(request):
    if not request.user.is_authenticated or not request.user.is_active:
        return redirect("login")

    user_watched_series_ids = Playlist.objects.filter(user=request.user).values_list('movies__id', flat=True)

    user_series_info = TVSeries.objects.filter(id__in=user_watched_series_ids).values_list('genre', 'imdb_rating')

    similar_series_query = TVSeries.objects.exclude(id__in=user_watched_series_ids)

    if not user_watched_series_ids:
        similar_series_query = TVSeries.objects.all()

    filter_conditions = Q()  
    for genre, imdb_rating in user_series_info:
        filter_conditions |= Q(genre__contains=genre, imdb_rating__gte=imdb_rating-0.5, imdb_rating__lte=imdb_rating+0.5)

    similar_series_query = similar_series_query.filter(filter_conditions)

    # Yeni eklenen diziye en benzeyeni al
    if user_watched_series_ids:
        latest_watched_series_id = user_watched_series_ids.latest('id')  
        latest_watched_series = TVSeries.objects.get(id=latest_watched_series_id)  
        most_similar_series = similar_series_query.annotate(
            similarity=F('imdb_rating') - latest_watched_series.imdb_rating
        ).order_by('-similarity').first()
        if most_similar_series:
            similar_series_query = similar_series_query.exclude(id=most_similar_series.id)

    similar_series_query = similar_series_query.annotate(
        similarity=F('imdb_rating') / (F('imdb_rating') + 1)  
    ).order_by('-similarity')

    recommended_series_ids = similar_series_query.values_list('id', flat=True)[:10]  
    recommended_series = TVSeries.objects.filter(id__in=recommended_series_ids)

    context = {'series_list': recommended_series}
    return render(request, 'movie_app/algorithm.html', context)


def view_playlists(request):
    playlists = Playlist.objects.filter(user=request.user)
    return render(request, 'movie_app/playlist.html', {'playlists': playlists})


def profile(request):
    return render(request, 'movie_app/profile_deneme.html')

    
@login_required
def profile_deneme(request):
    return render(request, 'movie_app/profile_deneme.html')


