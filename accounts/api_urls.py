from django.urls import path
from accounts.views import AccountActivationView

urlpatterns = [
    path('activate/', AccountActivationView.as_view(), name='activate'),
]