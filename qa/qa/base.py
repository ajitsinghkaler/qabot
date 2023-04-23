import json
import uuid

from django.db import models
from rest_framework.response import Response
from rest_framework import viewsets, status, serializers

class BaseModelViewSet(viewsets.ModelViewSet):
    def options(self, request, *args, **kwargs):
        """
        Self describing API. Allows for dynamic form generation.
        """
        meta = self.metadata_class()
        data = meta.determine_metadata(request, self)
        data.pop("description")
        return Response(json.dumps(data))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)




class BaseModel(models.Model):
    """
    Base model that all models inherit from.
    This model contains necessary fields and methods that all models require.
    """

    id = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False, primary_key=True
    )
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True

class BaseSerializer(serializers.ModelSerializer):
    def update(self, instance: object, validated_data: dict):
        # ensure we do not allow ID to update
        if "id" in validated_data.keys():
            validated_data.pop("id")
        return super().update(instance, validated_data)