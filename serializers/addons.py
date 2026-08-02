from rest_framework import serializers

class Token(serializers.Serializer):
    access_token = serializers.CharField()
    token_type = serializers.CharField()
    expires_in = serializers.CharField()

class StartSessionSerializer(serializers.Serializer):
    captcha = serializers.CharField(required=True, allow_blank=False)
