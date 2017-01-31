from rest_framework import routers

from api.rest import lectors, years
from api_textual.rest import news, texts

router = routers.DefaultRouter()
router.register(r'lectors', lectors.LectorViewSet)
router.register(r'news', news.NewsViewSet)
router.register(r'texts', texts.TextViewSet)
router.register(r'years', years.YearViewSet)
