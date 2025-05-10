from django.shortcuts import render
from rest_framework import generics, filters
from .models import UserComment
from .serializers import UserCommentSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

@method_decorator(cache_page(60), name='dispatch') # caching for 60 sec

class UserCommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = UserComment.objects.all().order_by('-created_at')
    serializer_class = UserCommentSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['username', 'email', 'created_at']
    ordering = ['-created_at']




