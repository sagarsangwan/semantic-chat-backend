from .views import ChatRoomViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()

router.register(r"chatrooms", ChatRoomViewSet, basename="chatroom")

urlpatterns = [path("", include(router.urls))]
