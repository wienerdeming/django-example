# REST framework
from rest_framework import routers

# Project
from apps.news.views import NewsCurdViewSet, NewsPublicView

app_name = 'apps.news'

router = routers.DefaultRouter()
router.register(r'news', NewsCurdViewSet, base_name='news')
router.register(r'news-public', NewsPublicView, base_name='news-public')

urlpatterns = router.urls
