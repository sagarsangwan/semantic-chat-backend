from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework import status

from .models import ChatMessage, ChatRoom
from .serializers import ChatRoomListSerializer, ChatRoomDetailsSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def all_chatrooms_view(request):
    if request.method == "GET":
        chatrooms = ChatRoom.objects.filter(participants=request.user)
        serializer = ChatRoomListSerializer(
            chatrooms, many=True, context={"request": request}
        )
        return Response(serializer.data)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def chatroom_view(request, chatroom_id):
    if request.method == "GET":
        print(chatroom_id)
        chatrooms = ChatRoom.objects.get(id=chatroom_id)
        serializer = ChatRoomDetailsSerializer(chatrooms, context={"request": request})
        return Response(serializer.data)
