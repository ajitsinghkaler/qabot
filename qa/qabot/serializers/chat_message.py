from qa.base import BaseSerializer

from rest_framework import serializers
from qabot.serializers.chat_history import ChatHistorySerializer
from qabot.models import ChatMessage


class ChatMessageSerializer(BaseSerializer):
    # id = serializers.CharField(required=False)
    # content = serializers.CharField(required=True)
    # chat_history = ChatHistorySerializer()
    # user_generated = serializers.BooleanField(required=True)

    class Meta:
        model = ChatMessage
        fields = '__all__'
