from rest_framework.permissions import IsAuthenticated
from .tasks import analyze_sentiment_task
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import ChatMessage, ChatRoom
from .serializers import (
    ChatRoomListSerializer,
    ChatRoomDetailsSerializer,
    ChatMessagesSerializer,
    ChatMessageCreateSerializer,
)
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
    elif request.method == "POST":
        data = request.data.copy()
        is_group = data.get("is_group", False)
        chatroom = ChatRoom.objects.create(
            name=data.get("name", None), is_group=is_group
        )
        chatroom.participants.add(request.user)
        participants = data.get("participants", [])

        if isinstance(participants, list):
            chatroom.participants.add(*participants)
        chatroom.save()
        serializer = ChatRoomDetailsSerializer(chatroom, contex=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def chatroom_view(request, chatroom_id):
    if request.method == "GET":
        print(chatroom_id)
        chatrooms = ChatRoom.objects.get(id=chatroom_id)
        serializer = ChatRoomDetailsSerializer(chatrooms, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_message_to_chatroom(request, chatroom_id):
    if request.method == "POST":
        data = request.data
        try:
            chatroom = ChatRoom.objects.get(id=chatroom_id)
        except:
            return Response(
                {"error": "room not available"}, status=status.HTTP_404_NOT_FOUND
            )
        if request.user not in chatroom.participants.all():
            return Response(
                {"error": "user is not a part of current room"},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = ChatMessageCreateSerializer(data=data)
        print(serializer)
        if serializer.is_valid():
            message_instance = serializer.save()
            print(message_instance)
            analyze_sentiment_task.delay(message_instance.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.error_messages)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POSt"])
@permission_classes([IsAuthenticated])
def search_query(request):
    if request.method == "POST":
        print(request.user.email)
        data = request.data
        query = data.get("query")
        print(query)
        chatrooms = ChatRoom.objects.filter(
            name__contains=query, participants=request.user
        )
        # user_chatrooms = chatrooms.filter()
        serializer = ChatRoomListSerializer(chatrooms)
        print(chatrooms)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def search_peoples(request):
    data = request.data
    query = data.get("query")
    users = User.objects.filter(email=query)
