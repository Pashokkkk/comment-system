from django.urls import path
from .views import UserCommentListCreateAPIView

urlpatterns = [
    path('comments/', UserCommentListCreateAPIView.as_view(), name='comment-list-create'),
]
