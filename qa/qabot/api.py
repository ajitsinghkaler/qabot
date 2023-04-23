from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
# from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from rest_framework.decorators import action
from rest_framework.response import Response

from qa.base import BaseModelViewSet
from qabot.models import Document, User, ChatMessage, ChatHistory
from qabot.serializers.chat_history import ChatHistorySerializer
from qabot.serializers.chat_message import ChatMessageSerializer


"""
def loadDocs():
    loader = TextLoader('./congoport.txt')
    index = VectorstoreIndexCreator().from_loaders([loader])
    query = "What is congoport looking for?"
    print(index.query(query))
    print(index.query_with_sources(query))
"""


class DocumentViewSet(BaseModelViewSet):
    search_fields = ["name"]
    ordering_fields = ["name", "updated", "created"]
    queryset = Document.objects.all()

class UserViewSet(BaseModelViewSet):
    queryset = User.objects.all()

class ChatViewSet(BaseModelViewSet):
    queryset = ChatHistory.objects.all()

    def list(self, request):
        queryset = ChatHistory.objects.filter(user_id=request.user.id)
        serializer = ChatHistorySerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def history(self, request):
        queryset = ChatMessage.objects.filter(ChatHistory_id=request.params.id)
        serializer = ChatMessageSerializer(queryset, many=True)

        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def answer(self, request):
        sender = self.request.data.get('question', None)
        return ""