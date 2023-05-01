from qa.base import BaseModel
from django.db import models
from django.contrib.auth.models import User

# class User(BaseModel):
#     """Customer user object"""

#     first_name = models.CharField(max_length=254, blank=False, null=False)
#     last_name = models.CharField(max_length=254, blank=False, null=False)

#     email = models.EmailField(
#         "unique email",
#         max_length=254,
#         unique=True,
#         null=False,
#         blank=False,
#         default="noreply@example.com",
#     )
#     phone_number = models.CharField(max_length=16, blank=True, null=True)
#     last_login = models.CharField(max_length=255, blank=True, null=True)

#     def __str__(self):
#         return f"{self.id} {self.first_name} {self.last_name}"

#     def get_full_name(self):
#         return f"{self.first_name} {self.last_name}"


class Document(BaseModel):
    title = models.CharField(max_length=255, null=False, blank=False)
    owner = models.ForeignKey(
        User, related_name="owner_files", on_delete=models.PROTECT, null=False
    )
    file = models.FileField(upload_to="documents/", null=False, blank=False)


class ChatHistory(BaseModel):
    sender = models.ForeignKey(
        User, related_name="chat_sender", on_delete=models.PROTECT, null=False
    )
    title = models.TextField()


class ChatMessage(BaseModel):
    content = models.TextField()
    user_generated = models.BooleanField(default=False)
    chat_history = models.ForeignKey(
        ChatHistory,
        related_name="chat_history",
        on_delete=models.PROTECT,
        null=False,
        default=1
    )
