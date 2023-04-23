from qa.base import BaseSerializer

from rest_framework import serializers
from qabot.serializers.user import UserSerializer
from qabot.models import Document

class DocumentSerializer(BaseSerializer):
    id = serializers.CharField(required=False)
    title = serializers.CharField(required=True)
    owner = UserSerializer()
    path = serializers.FileField() 
    class Meta:
        model = Document