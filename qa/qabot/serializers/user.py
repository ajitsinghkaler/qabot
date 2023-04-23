from qa.base import BaseSerializer

from rest_framework import serializers
from qabot.models import User

class UserSerializer(BaseSerializer):
    id = serializers.CharField(required=False)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField() 
    phone_number = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    last_login = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = User