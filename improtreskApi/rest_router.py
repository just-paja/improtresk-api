from rest_framework import routers

from api.rest import accomodations, lectors, workshops, years
from api_textual.rest import news, texts

router = routers.DefaultRouter()
router.register(r'lectors', lectors.LectorViewSet)
router.register(r'news', news.NewsViewSet)
router.register(r'texts', texts.TextViewSet)
router.register(r'years', years.YearViewSet)
router.register(r'workshops', workshops.WorkshopViewSet)
router.register(r'accomodations', accomodations.AccomodationViewSet)
