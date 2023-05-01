from qa.base import BaseSerializer

from rest_framework import serializers
from qabot.models import ChatHistory


class ChatHistorySerializer(BaseSerializer):
    # id = serializers.CharField(required=False)
    # content = serializers.CharField(required=True)
    # sender = UserSerializer()

    class Meta:
        model = ChatHistory
        fields = '__all__'
