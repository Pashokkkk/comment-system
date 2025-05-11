from django.urls import path
from .views import captcha_refresh, UserCommentListCreateAPIView

urlpatterns = [
    path('comments/', UserCommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('captcha/refresh/', captcha_refresh),
]
