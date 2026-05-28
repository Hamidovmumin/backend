from django.urls import path
from accounts.views import ActivateView

urlpatterns = [
    path('activate/', ActivateView.as_view(), name='activate-page'),
]