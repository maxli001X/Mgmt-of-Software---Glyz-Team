"""
MASTER URL ROUTING (Traffic Controller)

This file routes incoming URLs to the correct app:
- / → posting app (home feed)
- /auth/* → auth_landing app (login, signup)
- /moderation/* → moderation_ranking app
- /profile/* → profile_settings app
- /admin/ → Django admin panel

Each app has its own urls.py with detailed routes.

For more information: https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('auth_landing.urls', namespace='auth_landing')),
    path('', include('posting.urls', namespace='posting')),
    path('moderation/', include('moderation_ranking.urls', namespace='moderation_ranking')),
    path('profile/', include('profile_settings.urls', namespace='profile_settings')),
    path('972b69d/', include('analytics.urls')),
]

# Serve media files in both development and production
# Note: For production scale, consider using cloud storage (S3/Cloudinary)
# Using re_path to always serve media, not just in DEBUG mode
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
