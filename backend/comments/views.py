from rest_framework import generics, filters 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import UserComment
from .serializers import UserCommentSerializer

@api_view(['GET'])
def captcha_refresh(request):
    # Generate and return new CAPTCHA key and image URL
    new_key = CaptchaStore.generate_key()
    image_url = captcha_image_url(new_key)
    return Response({'key': new_key, 'image_url': image_url})

class UserCommentListCreateAPIView(generics.ListCreateAPIView):
    # Handle listing and creating top-level comments
    queryset = UserComment.objects.filter(parent_comment__isnull=True)
    serializer_class = UserCommentSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['username', 'email', 'created_at']
    ordering = ['-created_at']
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]
