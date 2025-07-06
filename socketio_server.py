import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "semantic_chat_backend.settings")

import django

django.setup()
import uuid
from asgiref.sync import sync_to_async
from chat.models import ChatMessage, ChatRoom  # now it works
from chat.tasks import analyze_sentiment_task
from chat.serializers import ChatMessageCreateSerializer, ChatMessagesSerializer
import socketio
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model

User = get_user_model()

connected_users = {}
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
socketio_app = socketio.ASGIApp(sio)


# 🧠 Room-based logic using room_id
@sio.event
async def connect(sid, environ, auth):
    print("🔌 New connection:", sid)
    print(" user auth token", auth)

    token = auth.get("token") if auth else None

    if not token:
        print("❌ No token provided")
        return False  # Deny connection

    try:
        jwt_auth = JWTAuthentication()
        validated_token = await sync_to_async(jwt_auth.get_validated_token)(token)
        user = await sync_to_async(jwt_auth.get_user)(validated_token)
        print(user)
    except Exception as e:
        print("❌ Invalid token:", e)
        return False  # Deny connection

    connected_users[sid] = user
    print(f"✅ {user.username} connected with sid {sid}")


@sio.event
async def join_room(sid, data):
    room_id = data.get("room_id")
    print(room_id, "//////////////////////////////////////")
    if room_id:
        await sio.enter_room(sid, room_id)
        print(f"{sid} joined room {room_id}")


@sio.event
async def chat_message(sid, data):
    print(sid)
    room_id = data.get("room")
    message_text = data.get("message")
    print(
        data,
        "///////////////////////////////////////////////////////////////////////",
    )
    if not room_id or not message_text:
        await sio.emit("error", {"error": "Missing room or message"}, to=sid)
        return

    try:
        chatroom = await sync_to_async(ChatRoom.objects.get)(id=room_id)
    except ChatRoom.DoesNotExist:
        await sio.emit("error", {"error": "Room not found"}, to=sid)
        return

    # Get the user from the session or sid (depending on your auth setup)
    user = connected_users.get(sid)  #

    is_participant = await sync_to_async(
        chatroom.participants.filter(id=user.id).exists
    )()
    if not user or not is_participant:
        await sio.emit("error", {"error": "Unauthorized"}, to=sid)
        return

    # # Optionally save the message to DB
    # message_instance = await sync_to_async(ChatMessage.objects.create)(
    #     room=chatroom,
    #     sender=user,
    #     message=message_text,
    #     timestamp=data.get("timestamp"),
    # )
    message_serializer = ChatMessageCreateSerializer(data=data)
    is_s_valid = await sync_to_async(message_serializer.is_valid)()

    if is_s_valid:
        message_instance = await sync_to_async(message_serializer.save)()
        print(message_instance)
        await sync_to_async(analyze_sentiment_task.delay)(message_instance.id)
    print(f"Message in room {room_id} by {user}: {message_text}")
    print(message_instance, "kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")

    # Serialize inside a sync wrapper
    def serialize_message(instance):
        return ChatMessagesSerializer(instance).data.copy()

    message_json = await sync_to_async(serialize_message)(message_instance)

    def convert_uuids(obj):
        if isinstance(obj, dict):
            return {k: convert_uuids(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_uuids(i) for i in obj]
        elif isinstance(obj, uuid.UUID):
            return str(obj)
        return obj

    message_json = await sync_to_async(serialize_message)(message_instance)
    message_json = convert_uuids(message_json)
    await sio.emit(
        "chat_message",
        message_json,
        room=room_id,
    )


@sio.event
async def disconnect(sid):
    user = connected_users.pop(sid, None)
    print(f"👋 Disconnected: {user.username if user else sid}")
