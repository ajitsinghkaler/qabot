import logging

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

from qa.base import BaseModelViewSet
from qa.settings import db_directory
from qabot.models import Document, User, ChatMessage, ChatHistory
from qabot.serializers.chat_history import ChatHistorySerializer
from qabot.serializers.chat_message import ChatMessageSerializer
from qabot.serializers.user import UserSerializer
from qabot.serializers.document import DocumentSerializer
from qabot.utils.load_docs_as_vector import load_docs_as_vector

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
            embeddings = OpenAIEmbeddings()
            vectordb = Chroma(persist_directory=db_directory, embedding_function=embeddings)
            retriever = vectordb.as_retriever()
            docs = retriever.get_relevant_documents(question)
            chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
            answer = chain.run(input_documents=docs, question=question)
            print(answer)
            return Response(
                {
                    "status": "success",
                    "answer": answer,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            log.error(e)
            return Response(
                {"status": "failure", "message": "Question could not be answered"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
