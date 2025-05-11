from rest_framework import serializers
from captcha.models import CaptchaStore
from .models import UserComment
import bleach

class UserCommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    captcha_text = serializers.CharField(write_only=True)
    captcha_key = serializers.CharField(write_only=True)

    class Meta:
        model = UserComment
        fields = [
            'id', 'username', 'email', 'homepage_url', 'text',
            'parent_comment', 'created_at', 'file_upload',
            'captcha_text', 'captcha_key', 'replies'
        ]
        read_only_fields = ['created_at', 'replies']

    def get_replies(self, obj):
        children = obj.replies.all().order_by('created_at')
        return UserCommentSerializer(children, many=True).data

    def validate_text(self, value):
        allowed_tags = ['a', 'code', 'i', 'strong']
        return bleach.clean(value, tags=allowed_tags, strip=True)

    def validate(self, data):
        key = data.get('captcha_key')
        text = data.get('captcha_text')

        if not key or not text:
            raise serializers.ValidationError({'captcha_text': 'CAPTCHA is required'})

        try:
            captcha = CaptchaStore.objects.get(hashkey=key)
        except CaptchaStore.DoesNotExist:
            raise serializers.ValidationError({'captcha_text': 'Невірна CAPTCHA.'})

        if captcha.response.lower() != text.strip().lower():
            raise serializers.ValidationError({'captcha_text': 'Невірна CAPTCHA.'})

        data.pop('captcha_key')
        data.pop('captcha_text')
        
        captcha.delete()

        return data