from rest_framework import serializers
from captcha.models import CaptchaStore
from .models import UserComment
from html.parser import HTMLParser
from django.core.exceptions import ValidationError
from .tasks import send_comment_email
import bleach

# Allow only specific HTML tags and attributes
ALLOWED_TAGS = ['a', 'code', 'i', 'strong']
ALLOWED_ATTRIBUTES = {'a': ['href', 'title']}


def validate_html(content):
    # Clean disallowed HTML tags
    cleaned = bleach.clean(content, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=False)
    if cleaned != content:
        raise ValidationError("HTML contains disallowed tags or attributes.")

    # Check if all HTML tags are properly closed
    class TagChecker(HTMLParser):
        def __init__(self):
            super().__init__()
            self.stack = []
            self.unclosed = False

        def handle_starttag(self, tag, attrs):
            if tag in ALLOWED_TAGS:
                self.stack.append(tag)

        def handle_endtag(self, tag):
            if tag in ALLOWED_TAGS:
                if not self.stack or self.stack[-1] != tag:
                    self.unclosed = True
                else:
                    self.stack.pop()

    checker = TagChecker()
    checker.feed(content)
    if checker.stack or checker.unclosed:
        raise ValidationError("HTML tags are not properly closed. Must be valid XHTML.")

    return cleaned


class UserCommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    captcha_text = serializers.CharField(write_only=True)
    captcha_key = serializers.CharField(write_only=True)
    file_upload = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = UserComment
        fields = [
            'id', 'username', 'email', 'homepage_url', 'text',
            'parent_comment', 'created_at', 'file_upload',
            'captcha_text', 'captcha_key', 'replies'
        ]
        read_only_fields = ['created_at', 'replies']

    def get_replies(self, obj):
        # Get and serialize child comments
        children = obj.replies.all().order_by('created_at')
        return UserCommentSerializer(children, many=True).data

    def validate_text(self, value):
        # Sanitize and validate HTML
        return validate_html(value)

    def validate(self, attrs):
        # Validate CAPTCHA input
        key = attrs.get('captcha_key')
        text = attrs.get('captcha_text')

        if not key or not text:
            raise serializers.ValidationError({'captcha_text': 'CAPTCHA is required'})

        try:
            captcha = CaptchaStore.objects.get(hashkey=key)
        except CaptchaStore.DoesNotExist:
            raise serializers.ValidationError({'captcha_text': 'Invalid CAPTCHA key.'})

        if captcha.response.lower() != text.strip().lower():
            raise serializers.ValidationError({'captcha_text': 'Incorrect CAPTCHA.'})

        # Remove used CAPTCHA
        captcha.delete()
        return attrs

    def create(self, validated_data):
        # Remove CAPTCHA fields before saving
        validated_data.pop('captcha_text', None)
        validated_data.pop('captcha_key', None)

        file = validated_data.get("file_upload")
        email = validated_data.get("email")
        text = validated_data.get("text")

        # Save the comment to DB
        comment = UserComment.objects.create(**validated_data)

        # Send email via Celery
        if email:
            send_comment_email.delay(email, text)

        return comment
