from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

# Create your views here.

from .models import ChatRoom
from .serializers import ChatRoomSerializer
from rest_framework.exceptions import PermissionDenied


# class
class ChatRoomViewSet(viewsets.ModelViewSet):
    # queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChatRoom.objects.filter(participants=self.request.user)

    def get_object(self):
        obj = super().get_object()
        if self.request.user not in obj.participants.all():
            raise PermissionDenied("You do not have access to ths room")
        return obj

    def perform_create(self, serializer):
        room = serializer.save()
        room.participants.add(self.request.user)
        if not room.is_group and not room.name:
            room.name = ", ".join([user.username for user in room.participants.all()])
            print(room.name)
            room.save()
