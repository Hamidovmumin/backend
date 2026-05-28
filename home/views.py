from django.shortcuts import render
from django.http import HttpRequest,HttpHeaders
from services.session import session_service
from crud.auth.registration import registration_crud

def home(request):
    return render(request, 'index/index.html')

def login(request):
    return render(request, 'auth/login.html')

def register(request: HttpRequest):
    return render(request,"auth/registration.html")

