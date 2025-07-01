import os
import django

# Set the Django settings module BEFORE any Django ORM or app code is imported/accessed
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "semantic_chat_backend.settings")
django.setup()  # Initialize Django apps here


from celery import shared_task
from .models import ChatMessage
import random


@shared_task
def analyze_sentiment_task(message_id):
    sentiments = [
        "neutral",
        "casual",
        "friendly",
        "supportive",
        "romantic",
        "happy",
        "tense",
        "argumentative",
        "angry",
        "sad",
        "anxious",
        "excited",
        "deep",
        "grateful",
        "stressed",
        "hopeful",
    ]
    try:
        print(message_id, "messagessssssssssssssssssssssssssssssssssssssssssssssss")
        message = ChatMessage.objects.get(id=message_id)
        sentiment_detected = random.choice(sentiments)
        print(sentiment_detected)
        message.sentiment = sentiment_detected
        message.toxicity_score = 0
        message.save()

    except ChatMessage.DoesNotExist:
        pass
