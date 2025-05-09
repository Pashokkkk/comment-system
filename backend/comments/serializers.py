from rest_framework import serializers
from .models import UserComment
import bleach

class UserCommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = UserComment
        fields = [
            'id', 'username', 'email', 'homepage_url', 'text',
            'parent_comment', 'created_at', 'file_upload', 'captcha_text',
            'replies'
        ]
        read_only_fields = ['created_at', 'replies']

    def get_replies(self, obj):
        children = obj.replies.all().order_by('created_at')
        return UserCommentSerializer(children, many=True).data

    def validate_text(self, value):
        allowed_tags = ['a', 'code', 'i', 'strong']
        return bleach.clean(value, tags=allowed_tags, strip=True)
