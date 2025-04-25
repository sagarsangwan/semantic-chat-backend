from django.db import models
from django.contrib.auth.models import User
import uuid


class ChatRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    participants = models.ManyToManyField(User, related_name="chat_rooms")
    is_group = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


SUMMARY_TAG_CHOICES = [
    ("neutral", "Neutral"),
    ("casual", "Casual"),
    ("friendly", "Friendly"),
    ("supportive", "Supportive"),
    ("romantic", "Romantic"),
    ("happy", "Happy"),
    ("tense", "Tense"),
    ("argumentative", "Argumentative"),
    ("angry", "Angry"),
    ("sad", "Sad"),
    ("anxious", "Anxious"),
    ("excited", "Excited"),
    ("deep", "Deep"),
    ("grateful", "Grateful"),
    ("stressed", "Stressed"),
    ("hopeful", "Hopeful"),
]

AI_SUGGESTION_FEEDBACK_CHOICES = [
    {"accepted", "Accepted"},
    {"rejected", "Rejected"},
    {"skipped", "Skipped"},
]


class ChatMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    is_read = models.BooleanField(default=False)
    edited = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    sentiment = models.CharField(
        max_length=20,
        choices=[
            ("positive", "Positive"),
            ("negative", "Negative"),
            ("neutral", "Neutral"),
        ],
        null=True,
        blank=True,
    )
    toxicity_score = models.FloatField(null=True, blank=True)
    ai_suggestion = models.TextField(null=True, blank=True)
    ai_suggestion_used = models.BooleanField(default=False)
    ai_suggestion_feedback = models.CharField(
        max_length=30, null=True, blank=True, choices=AI_SUGGESTION_FEEDBACK_CHOICES
    )
    summary_tag = models.CharField(
        max_length=30, null=True, blank=True, choices=SUMMARY_TAG_CHOICES
    )
    source = models.CharField(max_length=10, default="user")


class ChatSession(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    summary = models.TextField(blank=True, null=True)
    mood_overview = models.CharField(max_length=30, null=True, blank=True)
