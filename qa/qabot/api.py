import logging

from rest_framework.decorators import (
    action,
    permission_classes,
    authentication_classes,
    api_view,
)
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.middleware.csrf import get_token
from django.http import JsonResponse

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

from qa.base import BaseModelViewSet
from qa.settings import db_directory
from qabot.models import Document, ChatMessage, ChatHistory
from qabot.serializers.chat_history import ChatHistorySerializer
from qabot.serializers.chat_message import ChatMessageSerializer

# from qabot.serializers.user import UserSerializer
from qabot.serializers.document import DocumentSerializer
from qabot.utils.load_docs_as_vector import load_docs_as_vector

log = logging.getLogger(__name__)


class DocumentViewSet(BaseModelViewSet):
    search_fields = ["name"]
    ordering_fields = ["updated", "created"]
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


    def list(self, request):
        queryset = Document.objects.filter(owner=request.user.id).order_by("-created")
        serializer = DocumentSerializer(queryset, many=True)
        return Response(serializer.data)

    
    def create(self, request, *args, **kwargs):
        try:
            file = request.FILES.get("file", None)
            owner = request.user.id
            # owner = request.data.get("owner", None)
            if not file:
                return Response(
                    {"status": "failure", "message": "File not provided."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            request_data = {
                "title": file.name,
                "owner": owner,
                "file": file,
            }
            serializer = DocumentSerializer(data=request_data)
            
            if serializer.is_valid():
                load_docs_as_vector(file)
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


# class UserViewSet(BaseModelViewSet):
#     queryset = User.objects.all()


class ChatViewSet(BaseModelViewSet):
    queryset = ChatHistory.objects.all()
    ordering_fields = ["updated", "created"]
    serializer_class = ChatHistorySerializer

    def list(self, request):
        queryset = ChatHistory.objects.filter(sender=request.user.id).order_by("-created")
        serializer = ChatHistorySerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def history(self, request):
        try:
            queryset = ChatMessage.objects.filter(
                chat_history__id=request.query_params.get("id"),
                chat_history__sender=request.user.id,
            ).order_by("created")
            serializer = ChatMessageSerializer(queryset, many=True)

            return Response(
                {"status": "success", "history": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            log.error(e)
            return Response(
                {"status": "failure", "message": "Question could not be answered"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["post"])
    def answer(self, request):
        try:
            question = request.data.get("content")
            chat_history = request.data.get("chat_history")
            owner = request.user.id
            title = request.data.get("title") or "Untitled"
            if not chat_history:
                history_serializer = ChatHistorySerializer(
                    data={"sender": owner, "title": title}
                )
                if history_serializer.is_valid():
                    history = history_serializer.save()
            request_data = {
                "user_generated": True,
                "chat_history": chat_history,
                "content": question,
            }

            serializer = ChatMessageSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save()
            # user_message = ChatMessage(
            #     user_generated=True, chat_history=chat_history, content=question
            # )

            embeddings = OpenAIEmbeddings()
            vectordb = Chroma(
                persist_directory=db_directory, embedding_function=embeddings
            )
            retriever = vectordb.as_retriever()
            docs = retriever.get_relevant_documents(question)
            chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
            answer = chain.run(input_documents=docs, question=question)
            answer_data = {"chat_history": chat_history, "content": answer}
            # openai_message = ChatMessage(chat_history=chat_history, content=answer)
            answer_serializer = ChatMessageSerializer(data=answer_data)
            if answer_serializer.is_valid():
                computer = answer_serializer.save()
            return Response(
                {
                    "status": "success",
                    "answer": answer,
                    "history": (chat_history or history.id)
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            log.error(e)
            return Response(
                {"status": "failure", "message": "Question could not be answered"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication])
def csrf(request):
    try:
        return Response(
            {"csrfToken": get_token(request)},
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        log.error(e)
        return Response(
            {
                "status": "failure",
                "message": "A problem occured while getting the token",
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

def ping(request):
    return JsonResponse({"result": "OK"}, status=status.HTTP_200_OK)
