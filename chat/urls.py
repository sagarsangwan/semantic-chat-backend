from .views import chatroom_view, all_chatrooms_view
from django.urls import path

urlpatterns = [
    path("chatrooms/", all_chatrooms_view, name="chatroom_list_create_view"),
    path(
        "chatrooms/<uuid:chatroom_id>/", chatroom_view, name="chatroom_list_create_view"
    ),
]
