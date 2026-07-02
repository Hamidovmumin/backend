from datetime import timezone,datetime,timedelta
from django.contrib.auth.hashers import check_password
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from crud.user import user_crud
from utils.block import Throttle
from crud.auth.login import login_crud
from rest_framework.response import Response
from services.session import session_service
from django.conf import settings
from serializers.addons import Token
from serializers.auth.login import (
    LoginInformationRequest,
    LoginInformationResponse,
    LoginMfaResponse,
    LoginSelectMfaMethodResponse,
    LoginSelectMfaMethodRequest,
    LoginConfirmEmailCodeRequest,
    LoginConfirmEmailCodeResponse,
    LoginConfirmTotpCodeResponse,
    LoginConfirmTotpCodeRequest,
)
from deps.session import LoginAuthentication
from utils.bad_password import handle_failed_login_attempt
from utils.block import block_time
from choices.mfa_choices import validate_mfa_method
from utils.email_sms import send_email_sms
import pyotp
from django.contrib.auth import authenticate, login, logout
from utils.masked_email import masked_email
from rest_framework.permissions import IsAuthenticated
from core.security import verify_password
import time

@extend_schema(auth=[],tags=['Login'])
class StartSessionView(APIView):
    throttle_classes = [Throttle]
    authentication_classes = []
    throttle_group = 'login1'
    permission_classes = []

    def get(self, request: Request):
        data = session_service.start_session(
            request=request,
            crud=login_crud,
            rate_limit_minutes=settings.RATE_LIMIT_MINUTES,
            max_attempts=settings.MAX_ATTEMPTS,
        )

        serializer = Token(data)
        return Response(serializer.data)

@extend_schema(
    auth=[{"BearerAuth": []}],
    tags=['Login'],
    responses={200: LoginInformationResponse},
    request=LoginInformationRequest,
)
class ValidateInformation(APIView):
    throttle_classes = [Throttle]
    authentication_classes = [LoginAuthentication]
    throttle_group = 'login2'
    permission_classes = [AllowAny]

    def post(self, request: Request):
        t0 = time.perf_counter()
        login_session = request.user

        serializer = LoginInformationRequest(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        t1 = time.perf_counter()
        user = user_crud.get_by_username(username=username)
        print("db:", time.perf_counter() - t1)
        if not user:
            raise ValidationError('User not found')

        if not user.is_active:
            raise ValidationError('Account is not inactive')

        count = user.bad_password_count
        if user.block_time and user.block_time > datetime.now(timezone.utc):
            raise block_time(count=count)

        t2 = time.perf_counter()
        if verify_password(password, user.password):
            print("verify:", time.perf_counter() - t2)
            response_serializer = LoginInformationResponse(
                instance={
                    'username': user.username,
                    'password': True
                }
            )
            login_crud.update(db_obj=login_session,user_id=user.id,password_is_validated=True)

            return Response(response_serializer.data)

        else:
            raise handle_failed_login_attempt(account = user)



@extend_schema(
    auth=[{"BearerAuth": []}],
    tags=['Login'],
    responses={200: LoginMfaResponse},
)
class ValidateMfaMethod(APIView):
    throttle_classes = [Throttle]
    authentication_classes = [LoginAuthentication]
    throttle_group = 'login3'
    permission_classes = [AllowAny]

    def get(self,request:Request):
        login_session = request.user

        if not login_session.password_is_validated:
            raise ValidationError('Password is not valid')

        response_serializer = LoginMfaResponse(
            instance={
                "masked_email": masked_email(login_session.user.email) if login_session.user.email_is_confirmed else None,
                'email': True if login_session.user.email_is_confirmed else False,
                'totp': True if login_session.user.totp_is_confirmed else False,
            }
        )
        return Response(response_serializer.data)


@extend_schema(
    auth=[{"BearerAuth": []}],
    tags=['Login'],
    responses={200: LoginSelectMfaMethodResponse},
    request=LoginSelectMfaMethodRequest,
)
class SelectMfaMethod(APIView):
    throttle_classes = [Throttle]
    authentication_classes = [LoginAuthentication]
    throttle_group = 'login4'
    permission_classes = [AllowAny]

    def post(self,request: Request):
        login_session = request.user

        serializer = LoginSelectMfaMethodRequest(data=request.data)
        serializer.is_valid(raise_exception=True)

        mfa_method = serializer.validated_data.get('mfa_method')

        validate_mfa_method(value=mfa_method)
        code_expire_at = datetime.now(timezone.utc) + timedelta(minutes=15) if mfa_method =="totp" else None
        login_crud.update(db_obj=login_session,mfa_method=mfa_method,code_expire_at = code_expire_at)

        response_serializer = LoginSelectMfaMethodResponse(
            instance={
                'mfa_method':mfa_method
            }
        )
        return Response(response_serializer.data)


@extend_schema(
    auth=[{"BearerAuth": []}],
    tags=['Login'],
)
class LoginSendEmailCode(APIView):
    throttle_classes = [Throttle]
    authentication_classes = [LoginAuthentication]
    throttle_group = 'login5'
    permission_classes = [AllowAny]

    def post(self,request: Request):
        login_session = request.user

        if str(login_session.mfa_method) != 'email':
            raise ValidationError('Mfa method is not email')

        if not login_session.user.email_is_confirmed:
            raise ValidationError('Email doğrulanması düzgün deyil!')

        send_email_sms(request=request,email_type='mfa_code',account=login_session)

        return Response({'status': 'success'})


@extend_schema(
    auth=[{"BearerAuth": []}],
    tags=['Login'],
    responses={200: LoginConfirmEmailCodeResponse},
    request=LoginConfirmEmailCodeRequest,
)
class LoginConfirmedEmailCode(APIView):
    throttle_classes = [Throttle]
    authentication_classes = [LoginAuthentication]
    throttle_group = 'login6'
    permission_classes = [AllowAny]

    def post(self,request: Request):
        login_session = request.user

        serializer = LoginConfirmEmailCodeRequest(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data.get('code')

        if login_session.code_expire_at < datetime.now(timezone.utc):
            raise ValidationError('Kodun müddəti bitmişdir!')

        if not login_session.email_code:
            raise ValidationError('Email kodu göndərilməyib!')

        if login_session.email_code != code:
            raise ValidationError('Daxil edilmiş kod səhvdir!')

        if login_session.email_code == code:
            login_crud.update(db_obj=login_session,email_code=None,code_expire_at=None,email_code_confirmed=True)

        response_serializer = LoginConfirmEmailCodeResponse(
            instance={
                'code': True,
            }
        )
        return Response(response_serializer.data)



@extend_schema(
    auth=[{"BearerAuth": []}],
    tags=['Login'],
    responses={200: LoginConfirmTotpCodeResponse},
    request=LoginConfirmTotpCodeRequest,
)
class LoginConfirmedTotpCode(APIView):
    throttle_classes = [Throttle]
    authentication_classes = [LoginAuthentication]
    throttle_group = 'login7'
    permission_classes = [AllowAny]

    def post(self,request: Request):
        login_session = request.user
        serializer = LoginConfirmTotpCodeRequest(data=request.data)
        serializer.is_valid(raise_exception=True)

        if str(login_session.mfa_method) != 'totp':
            raise ValidationError('Mfa method is not totp')

        if login_session.code_expire_at < datetime.now(timezone.utc):
            raise ValidationError('Kodun müddəti bitmişdir!')

        totp_code = serializer.validated_data.get('totp_code')
        totp = pyotp.TOTP(login_session.user.totp_token)

        if not totp.verify(totp_code):
            raise ValidationError({
                'message': "Daxil edilmiş TOTP kodu səhvdir!"
            })

        login_crud.update(db_obj=login_session,totp_code_confirmed=True,code_expire_at=None)
        response_serializer = LoginConfirmTotpCodeResponse(
            instance={
                'totp_code': True,
            }
        )
        return Response(response_serializer.data)

@extend_schema(
    auth=[{"BearerAuth": []}],
    tags=['Login'],
)
class LoginFinish(APIView):
    throttle_classes = [Throttle]
    authentication_classes = [LoginAuthentication]
    throttle_group = 'login8'
    permission_classes = [AllowAny]

    def post(self,request: Request):
        login_session = request.user

        if str(login_session.mfa_method) == 'email':
            if not login_session.email_code_confirmed:
                raise ValidationError({
                    'error': "Email Doğrulaması səhvdir!"
                })

        if str(login_session.mfa_method) == 'totp':
            if not login_session.totp_code_confirmed:
                raise ValidationError({
                    'error': "TOTP Doğrulaması səhvdir!"
                })

        user = login_session.user
        login_crud.delete(db_obj=login_session)
        login(request, user)

        return Response({
            "message": "Login uğurludur"
        })



@extend_schema(
    auth=[{"SessionAuth": []}],
    tags=['Login'],
)
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)

        return Response(True)
