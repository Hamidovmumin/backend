from django.urls import path
from home.views import home,register,login,page_404

urlpatterns = [
    path('', home, name='home'),
    path('404/', register, name='error404'),
    path('login/', login, name='login'),
    path('registration/', register, name='registration'),
]