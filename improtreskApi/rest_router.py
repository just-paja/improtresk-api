from rest_framework import routers

from api.rest import serializers
from api_textual.rest import texts

router = routers.DefaultRouter()
router.register(r'texts', texts.TextViewSet)
router.register(r'years', serializers.YearSet)
