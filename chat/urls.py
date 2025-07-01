from .views import (
    chatroom_view,
    all_chatrooms_view,
    send_message_to_chatroom,
    search_query,
)
from django.urls import path

urlpatterns = [
    path("chatrooms/", all_chatrooms_view, name="all_chatrooms_view"),
    path("chatrooms/<uuid:chatroom_id>/", chatroom_view, name="chatroom_view"),
    path(
        "chatrooms/send-message/<uuid:chatroom_id>/",
        send_message_to_chatroom,
        name="send_message_to_chatroom",
    ),
    path("search/", search_query, name="search_query"),
]
