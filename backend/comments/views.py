from rest_framework import generics, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore

from .models import UserComment
from .serializers import UserCommentSerializer

# CAPTCHA Refresh API
@api_view(['GET'])
def captcha_refresh(request):
    new_key = CaptchaStore.generate_key()
    image_url = captcha_image_url(new_key)
    return Response({'key': new_key, 'image_url': image_url})

# Основний API для коментарів
@method_decorator(cache_page(60), name='dispatch')  # Кешування на 60 секунд
class UserCommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = UserComment.objects.all().order_by('-created_at')
    serializer_class = UserCommentSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['username', 'email', 'created_at']
    ordering = ['-created_at']
