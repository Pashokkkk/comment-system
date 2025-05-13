from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import never_cache
import logging
from comments.views import UserCommentListCreateAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Define API and admin routes
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('comments.urls')),
    path('api/comments/', UserCommentListCreateAPIView.as_view()),
    path('captcha/', include('captcha.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Catch-all route for SPA (e.g., Vue, React)
urlpatterns += [
    re_path(r'^.*$', never_cache(TemplateView.as_view(template_name='index.html'))),
]
