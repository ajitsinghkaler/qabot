from qa.base import BaseSerializer

from rest_framework import serializers
# from qabot.serializers.user import UserSerializer
from qabot.models import Document


class DocumentSerializer(BaseSerializer):
    class Meta:
        model = Document
        fields = '__all__'
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('owner')  # Remove the 'owner' field from the response
        return data
    
