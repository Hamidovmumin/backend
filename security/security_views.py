from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.core import signing
from rest_framework.response import Response
from django.shortcuts import redirect
from django.contrib.sessions.models import Session
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class SecurityLogoutView(APIView):

    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, token):

        try:
            data = signing.loads(
                token,
                salt="login-alert",
                max_age=60 * 60 * 24,
            )

        except signing.BadSignature:

            return redirect("home")

        session_key = data["session_key"]

        session = Session.objects.filter(
            session_key=session_key
        ).first()

        if session:
            session.delete()

            channel_layer = get_channel_layer()

            async_to_sync(
                channel_layer.group_send
            )(
                f"session_{session_key}",
                {
                    "type": "force_logout",
                },
            )

        return redirect("home")