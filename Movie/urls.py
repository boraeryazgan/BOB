from django.urls import path
from .views import login_view, signup, logout_view,index

urlpatterns = [
    path('', index, name='index'),

    path('login/', login_view, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', logout_view, name='logout'),
]
