from django.urls import path
from .views import login_view, signup, logout_view,index,detail,search

urlpatterns = [
    path('', index, name='index'),
    path('search/', search, name='search'),  # Arama işlevi için URL yönlendirmesi

    path('login/', login_view, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('detail/<int:serie_id>/', detail, name='detail'),

]
