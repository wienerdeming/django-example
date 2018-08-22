# Django
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

# REST framework
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('', include_docs_urls(title='GS1 API')),
    path('admin/', admin.site.urls),
    path('api/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/v1/', include('apps.gauth.urls', namespace='apps.gauth')),
    path('api/v1/', include('apps.news.urls', namespace='apps.news')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
