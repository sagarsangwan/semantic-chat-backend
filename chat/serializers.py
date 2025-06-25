from rest_framework import serializers


from .models import ChatMessage, ChatRoom
from django.contrib.auth.models import User

from allauth.socialaccount.models import SocialAccount


class SocialAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialAccount
        fields = ["extra_data"]
        read_only = True  # These fields are typically managed by allauth


class UserSerializer(serializers.ModelSerializer):
    social_accounts = SocialAccountSerializer(
        many=True, read_only=True, source="socialaccount_set"
    )

    class Meta:
        model = User
        # fields = ["id", "username", "email", "username", "picture"]
        fields = ["id", "username", "social_accounts"]


class ChatRoomListSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    other_participant = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        # fields = "__all__"
        fields = [
            "id",
            "participants",
            "name",
            "is_group",
            "created_at",
            "updated_at",
            "slug",
            "other_participant",
        ]

    def get_other_participant(self, obj):
        """
        Returns the serialized details of the other participant in a one-on-one chat room.
        """
        if obj.is_group:
            return None

        request = self.context.get("request")
        if request and request.user.is_authenticated:
            current_user = request.user
            other_participant = None
            for participant in obj.participants.all():
                if participant != current_user:
                    other_participant = participant
                    break
            if other_participant:
                serializer = UserSerializer(other_participant, context=self.context)

                return serializer.data
                # return other_participant.social_account.extra_data
        return None


class ChatMessagesSerializer(serializers.ModelSerializer):
    # participants = UserSerializer(many=True, read_only=True)
    # chatroom = ChatRoomSerializer(read_only=True)
    sender = UserSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        # fields = "__all__"
        fields = "__all__"


class ChatRoomDetailsSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    other_participant = serializers.SerializerMethodField()
    messages = ChatMessagesSerializer(many=True)

    class Meta:
        model = ChatRoom
        fields = "__all__"

    def get_other_participant(self, obj):
        """
        Returns the serialized details of the other participant in a one-on-one chat room.
        """
        if obj.is_group:
            return None

        request = self.context.get("request")
        if request and request.user.is_authenticated:
            current_user = request.user
            other_participant = None
            for participant in obj.participants.all():
                if participant != current_user:
                    other_participant = participant
                    break
            if other_participant:
                serializer = UserSerializer(other_participant, context=self.context)

                return serializer.data
                # return other_participant.social_account.extra_data
        return None
