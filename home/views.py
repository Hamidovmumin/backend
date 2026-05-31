
from django.http import Http404, HttpRequest
from django.shortcuts import render
from django.core.cache import cache
from utils.ip_address import get_ip

def home(request):
    return render(request, 'index/index.html')

def login(request):
    return render(request, 'auth/login.html')

def register(request: HttpRequest):
    ip_address = get_ip(request)
    block_key = f"rl:registration:blocked:{ip_address}"

    if cache.get(block_key):
        return render(request, '404.html')

    return render(request,"auth/registration.html")

def page_404(request: HttpRequest):
    return render(request, "404.html",status=404)
