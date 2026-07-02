from django.urls import path
from home.views import home,register,login,page_404,logout_account,books_all_page

urlpatterns = [
    path('', home, name='home'),
    path('404/', page_404, name='error404'),
    path('login/', login, name='login'),
    path('registration/', register, name='registration'),
    path('logout/', logout_account, name='logout'),
    path('books/', books_all_page, name='books-all'),
]