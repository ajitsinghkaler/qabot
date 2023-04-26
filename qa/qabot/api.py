import logging

# from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from qa.base import BaseModelViewSet
from qabot.models import Document, User, ChatMessage, ChatHistory
from qabot.serializers.chat_history import ChatHistorySerializer
from qabot.serializers.chat_message import ChatMessageSerializer
from qabot.serializers.user import UserSerializer
from qabot.serializers.document import DocumentSerializer
from qabot.utils.load_docs import load_docs

log = logging.getLogger(__name__)

class DocumentViewSet(BaseModelViewSet):
    search_fields = ["name"]
    ordering_fields = ["name", "updated", "created"]
    queryset = Document.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            file = request.FILES.get("file", None)
            if not file:
                return Response(
                    {"status": "failure", "message": "File not provided."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            request_data = {
                "title": file.name,
                "owner": request.data.get('owner', None),
                "file": file,
            }
            serializer = DocumentSerializer(data=request_data)
            if serializer.is_valid():
                document = serializer.save()
                return Response(
                    {
                        "status": "success",
                        "document": serializer.data,
                        "message": "File uploaded successfully",
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {
                        "status": "failure",
                        "message": "File could not be uploaded",
                        "errors": serializer.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            log.error(e)
            return Response(
                {"status": "failure", "message": "File could not be uploaded"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


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
        try:
            question = request.data.get("question")
            document_id = request.data.get("document_id")
            document = Document.objects.get(id=document_id)
            # index = chroma_db.get_index(document_id)
            # answer = index.query(question)
            # print(answer)
            return Response(
                {
                    "status": "success",
                    "message": "File uploaded successfully",
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            log.error(e)
            return Response(
                {"status": "failure", "message": "Question could not be answered"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
