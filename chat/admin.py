from django.contrib import admin

# Register your models here.
from .models import ChatMessage, ChatRoom, ChatSession


admin.site.register(ChatMessage)
admin.site.register(ChatRoom)
admin.site.register(ChatSession)
