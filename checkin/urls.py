from django.conf.urls import url
from .views import checkin

urlpatterns = [
    url(r'^(?P<code>[a-z0-9]+)', checkin),
]
