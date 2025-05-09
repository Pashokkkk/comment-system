from django.shortcuts import render
from rest_framework import generics, filters
from .models import UserComment
from .serializers import UserCommentSerializer

class UserCommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = UserComment.objects.all().order_by('-created_at')
    serializer_class = UserCommentSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['username', 'email', 'created_at']
    ordering = ['-created_at']


