from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserComment
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json
from .serializers import UserCommentSerializer

@receiver(post_save, sender=UserComment)
def notify_new_comment(sender, instance, created, **kwargs):
    if created:
        # Get WebSocket channel layer
        channel_layer = get_channel_layer()

        # Serialize the new comment
        data = UserCommentSerializer(instance).data

        # Send the comment to the "comments" group
        async_to_sync(channel_layer.group_send)(
            "comments",
            {
                "type": "comment_message",
                "message": json.dumps(data)
            }
        )
