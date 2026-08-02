from rest_framework.views import APIView
from crud.auth.registration import registration_crud
from crud.user import user_crud
from deps.session import RegistrationAuthentication
from django.contrib.auth.hashers import make_password
from services.session import session_service
import time
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from serializers.auth.registration import (
    RegistrationUsernameRequest,
    RegistrationUsernameResponse,
    RegistrationEmailRequest,
    RegistrationEmailResponse,
    RegistrationTOTPResponse,
    RegistrationConfirmTOTPRequest,
    RegistrationConfirmTOTPResponse,
    RegistrationPasswordResponse,
    RegistrationPasswordRequest,
    CreateAccountResponse
)
from rest_framework.response import Response
from rest_framework.request import Request
from serializers.addons import Token
from rest_framework.exceptions import ValidationError
import pyotp
from utils.email_sms import send_email_sms
from django.core.cache import cache
from django.conf import settings
from utils.block import Throttle
from core.security import get_password_hash

@extend_schema(auth=[],tags=['Registration'])
class StartSessionView(APIView):
    throttle_classes = [Throttle]
    throttle_group = 'registration_session'
    authentication_classes = []
    permission_classes = []

    def get(self, request: Request):

        data = session_service.start_session(
            request=request,
            crud=registration_crud,
            rate_limit_minutes=settings.RATE_LIMIT_MINUTES,
            max_attempts=settings.MAX_ATTEMPTS,
        )

        serializer = Token(data)
        return Response(serializer.data)


@extend_schema(
    auth=[{"BearerAuth": []}],
    tags=['Registration'],
    responses={200: RegistrationUsernameResponse},
    request=RegistrationUsernameRequest,
)
class ValidateUsername(APIView):
    throttle_classes = [Throttle]
    throttle_group = 'registration_validate'
    authentication_classes = [RegistrationAuthentication]
    permission_classes = [AllowAny] # IsAuthenticated


    # pip install django-redis

    def post(self, request):
        registration_session = request.user
        print('Endpoint:' + request.META.get('REMOTE_ADDR'))

        serializer = RegistrationUsernameRequest(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get("username")
        first_name = serializer.validated_data.get("first_name", "").strip()
        last_name = serializer.validated_data.get("last_name", "").strip()

        if not first_name or not last_name:
            raise ValidationError({
                "message": "Ad və Soyad boş ola bilməz."
            })

        user = user_crud.get_by_username(username=username)
        if user:
            raise ValidationError({
                "message": f"{username}-dən artıq istifadə olunub"
            })

        user_registration = registration_crud.get_by_username(username=username)
        if user_registration:
            raise ValidationError({
                "message": f'{username} -dən istifadə etməyə icazə yoxdur!'
            })

        registration_crud.update(
            db_obj=registration_session,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        response_serializer = RegistrationUsernameResponse(
            instance={
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
            }
        )

        return Response(response_serializer.data)


@extend_schema(
    auth=[{"BearerAuth": []}],
    tags=['Registration'],
    responses={200: RegistrationEmailResponse},
    request=RegistrationEmailRequest,
)
class ValidateEmail(APIView):
    throttle_classes = [Throttle]
    throttle_group = 'registration_email'
    authentication_classes = [RegistrationAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        registration_session = request.user

        serializer = RegistrationEmailRequest(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email").strip()

        user = user_crud.get_by_email(email)
        if user:
            raise ValidationError({"message": f'{email} e-poçtu artıq istifadə olunub!'})

        user_registration = registration_crud.get_by_email(email)
        if user_registration:
            raise ValidationError({"message": f'{email} -dən istifadə etməyə icazə yoxdur!'})

        registration_crud.update(
            db_obj=registration_session,
            email = email,
        )

        response_serializer = RegistrationEmailResponse(
            instance={
                "email": email,
            }
        )

        return Response(response_serializer.data)


@extend_schema(
    auth=[{"BearerAuth": []}],
    tags=['Registration'],
    responses={200: RegistrationTOTPResponse},
)
class ValidateTOTP(APIView):
    throttle_classes = [Throttle]
    throttle_group = 'registration_totp'
    authentication_classes = [RegistrationAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        registration_session = request.user

        if not registration_session.email:
            raise ValidationError({"message": f'email daxil edilməyib!'})

        # pip install pyotp
        totp_token = pyotp.random_base32()
        totp = pyotp.TOTP(totp_token)
        totp_token_qr_uri = totp.provisioning_uri(
            name=registration_session.username,
            issuer_name='novelora.az',
        )

        registration_crud.update(
            db_obj=registration_session,
            totp_token=totp_token,
            totp_token_qr_uri=totp_token_qr_uri,
        )

        response_serializer = RegistrationTOTPResponse(
            instance={
                "totp_token": totp_token,
                "totp_token_qr_uri": totp_token_qr_uri,
            }
        )

        return Response(response_serializer.data)


@extend_schema(
    auth=[{"BearerAuth": []}],
    tags=['Registration'],
    responses={200: RegistrationConfirmTOTPResponse},
    request=RegistrationConfirmTOTPRequest,
)
class ConfirmTOTP(APIView):
    throttle_classes = [Throttle]
    throttle_group = 'registration_confirm_totp'
    authentication_classes = [RegistrationAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        registration_session = request.user
        serializer = RegistrationConfirmTOTPRequest(data=request.data)
        serializer.is_valid(raise_exception=True)

        totp_code = serializer.validated_data.get("totp_code")

        totp = pyotp.TOTP(registration_session.totp_token)

        if not totp.verify(totp_code):
            raise ValidationError({
                'message': "Daxil edilmiş TOTP kodu səhvdir!"
            })

        registration_crud.update(
            db_obj=registration_session,
            totp_is_confirmed=True,
        )

        response_serializer = RegistrationConfirmTOTPResponse(
            instance={
                "totp_confirm": True,
            }
        )
        return Response(response_serializer.data)

@extend_schema(
    auth=[{"BearerAuth": []}],
    tags=['Registration'],
    responses={200: RegistrationPasswordResponse},
    request=RegistrationPasswordRequest,
)
class ValidatePassword(APIView):
    throttle_classes = [Throttle]
    throttle_group = 'registration_password'
    authentication_classes = [RegistrationAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        t0 = time.perf_counter()

        registration_session = request.user
        print("auth/user:", time.perf_counter() - t0)

        serializer = RegistrationPasswordRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        print("serializer:", time.perf_counter() - t0)

        password = serializer.validated_data.get("password")
        repeat_password = serializer.validated_data.get("repeat_password")

        if str(password) != str(repeat_password):
            raise ValidationError({
                'message': "Daxil edilmiş parollar eyni deyildir!"
            })

        hashed_password = get_password_hash(password)
        print("hash:", time.perf_counter() - t0)

        registration_crud.update(
            db_obj=registration_session,
            password=hashed_password,
            password_is_confirmed=True,
        )
        print("db update:", time.perf_counter() - t0)

        response_serializer = RegistrationPasswordResponse(
            instance={
                "password_confirmed": True,
            }
        )
        return Response(response_serializer.data)


@extend_schema(
    auth=[{"BearerAuth": []}],
    tags=['Registration'],
    responses={200:CreateAccountResponse}
)

class CreateUser(APIView):
    throttle_classes = [Throttle]
    throttle_group = 'registration'
    authentication_classes = [RegistrationAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):

        registration_session = request.user

        if not registration_session.password_is_confirmed:
            raise ValidationError({
                'message': "Parol təsdiq olunmayıb!"
            })

        user_crud.create(
            username=registration_session.username,
            email=registration_session.email,
            email_is_confirmed = registration_session.email_is_confirmed,
            password=registration_session.password,
            first_name=registration_session.first_name,
            last_name=registration_session.last_name,
            phone_number = str(+994775953058),
            totp_token = registration_session.totp_token,
            totp_is_confirmed = registration_session.totp_is_confirmed,
        )

        response_serializer = CreateAccountResponse(
            instance={
                "create_account":True
            }
        )


        return Response({
            "message": "Hesab ugurla yaradıldı",
            "data":response_serializer.data
        })


@extend_schema(
    auth=[{"BearerAuth": []}],
    tags=['Registration'],
)
class SendEmailSMS(APIView):
    throttle_classes = [Throttle]
    throttle_group = 'registration_sms'
    authentication_classes = [RegistrationAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):

        registration_session = request.user

        user = user_crud.get_by_username(username=registration_session.username)
        registration_crud.delete(db_obj=registration_session)

        send_email_sms(request,email_type='activation',account =user)

        return Response({
            "message": "Email göndərildi.",
            "sent": True,
        })




