from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<code>[a-z0-9]+)$', views.participant_checkin, name='checkin'),
    url(r'^(?P<code>[a-z0-9]+)/pay', views.participant_paid, name="checkin_pay"),
    url(r'^(?P<code>[a-z0-9]+)/check', views.participant_check, name="checkin_check"),
    url(r'^(?P<code>[a-z0-9]+)/refund', views.participant_refunded, name="checkin_refund"),
]
