from django.urls import path
from .views import login_view, signup, logout_view,index,detail,search,review_rate,add_to_liked_list,add_to_playlist, recommend_similar_series,view_playlists,profile_deneme

urlpatterns = [
    path('', index, name='index'),
    path('search/', search, name='search'),
    path('recommend',recommend_similar_series,name="recommend"),
    path('login/', login_view, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('detail/<int:serie_id>/', detail, name='detail'),
    path('review/', review_rate, name='review'),
    path('add_to_liked_list/',add_to_liked_list,name='add_to_liked_list'),
    path('add_to_playlist/', add_to_playlist, name='add_to_playlist'),
    path('playlists/', view_playlists, name='view_playlists'),
    path('profile_deneme/', profile_deneme, name='profile_deneme'),
]
