import json

from django.views.generic import TemplateView
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import render , reverse, redirect
from rest_framework.permissions import IsAuthenticated

from crud.user import user_crud
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core import signing
from django.core.cache import cache
from django.http import Http404
from rest_framework.exceptions import ValidationError
from cryptography.fernet import Fernet,InvalidToken
from myproject.settings import FERNET_KEY
from django.contrib.auth.tokens import default_token_generator

class ActivateView(TemplateView):
    authentication_classes = [TokenAuthentication]
    template_name = 'account/activate.html'

    def dispatch(self, request, *args, **kwargs):
        ip = request.META.get('REMOTE_ADDR') or 'unknown'

        block_key = f"rl:activate:blocked:{ip}"

        if cache.get(block_key):
            raise Http404

        payload = request.GET.get('payload')

        if not payload:
            raise Http404

        if len(payload) > 2000:
            raise Http404

        return super().dispatch(request, *args, **kwargs)



class AccountActivationView(APIView):
    authentication_classes = [TokenAuthentication]

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        if request.method == 'GET':
            ip = request.META.get('REMOTE_ADDR') or 'unknown'

            count_key = f"rl:activate:count:{ip}"
            block_key = f"rl:activate:blocked:{ip}"

            if cache.get(block_key):
                print("BLOCKED")
                raise Http404

            count = cache.get(count_key)

            if count is None:
                cache.set(count_key, 1, timeout=60)
                count = 1
            else:
                try:
                    count = cache.incr(count_key)
                except ValueError:
                    cache.set(count_key, 1, timeout=60)
                    count = 1

            print("COUNT:", count)

            if count > 5:
                cache.set(block_key, True, timeout=10)
                print("NOW BLOCKED")
                raise Http404



    def get(self,request):
        payload = request.GET.get('payload')
        if not payload:
            print("1-ci")
            raise ValidationError({
                "error": "Payload is required",
            })


        try:
            data = signing.loads(payload,max_age=72000)
        except signing.SignatureExpired:
            print("2-ci")
            raise ValidationError({
                "time":'Session müddəti bitmişdir.'
            })

        except signing.BadSignature:
            print("3-ci")
            raise ValidationError({
                "error": "Payload is invalid",
            })


        try:
            cipher = Fernet(FERNET_KEY.encode())
        except ValueError:
            print("4-ci")
            raise ValidationError({
                "error": "Fernet key düzgün deyil"
            })

        try:
            decrypted_data = cipher.decrypt(data['uid'].encode())
            uid = json.loads(decrypted_data.decode())
            user = user_crud.get_by_username(username=uid['username'])
        except (TypeError, ValueError, KeyError,InvalidToken):
            print("5-ci")
            raise ValidationError({
                "error":'Keçərsiz melumatlar!'
            })

        if not user:
            raise ValidationError({
                "error": "İstifadəçi tapılmadı"
            })

        if not data.get('token'):
            print("6-ci")
            raise ValidationError({
                "error":'Invalid Token'
            })

        if user is not None and default_token_generator.check_token(user, data['token']):
            user_crud.update(db_obj=user,email_is_confirmed=True, is_active=True)


        return Response({
            "sacsessful": "Hesab uğurla aktiv edildi"
        })


