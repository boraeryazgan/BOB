from django.urls import path
from .views import login_view, signup, logout_view,index,detail,search,review_rate,add_to_liked_list

urlpatterns = [
    path('', index, name='index'),
    path('search/', search, name='search'),

    path('login/', login_view, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('detail/<int:serie_id>/', detail, name='detail'),
    path('review/', review_rate, name='review'),
    path('add_to_liked_list/',add_to_liked_list,name='add_to_liked_list')
]
