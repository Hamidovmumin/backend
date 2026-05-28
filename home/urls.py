from django.urls import path
from home.views import home,register,login

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('registration/', register, name='registration'),
]