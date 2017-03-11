from api.rest import accomodations, lector_roles, lectors, orders, participants, rules,\
    schedule, workshop_difficulties, workshops, years
from api_textual.rest import news, performers, texts, workshop_locations

from rest_framework import routers

from rest_framework_extensions.routers import NestedRouterMixin


class NestedDefaultRouter(NestedRouterMixin, routers.DefaultRouter):
    pass


router = NestedDefaultRouter()
router.register(r'lectorRoles', lector_roles.LectorRoleViewSet)
router.register(r'lectors', lectors.LectorViewSet)
router.register(r'news', news.NewsViewSet)
router.register(r'orders', orders.OrderViewSet)
router.register(r'texts', texts.TextViewSet)
router.register(r'workshopDifficulties', workshop_difficulties.WorkshopDifficultyViewSet)
router.register(r'years', years.YearViewSet)
router.register(
    r'years/(?P<year>[0-9]{4})/workshops',
    workshops.WorkshopViewSet,
    base_name='workshops',
).register(
    r'participants',
    participants.ParticipantViewSet,
    base_name='workshops-participants',
    parents_query_lookups=['assigned_workshop'],
)
router.register(
    r'years/(?P<year>[0-9]{4})/locations',
    workshop_locations.WorkshopLocationViewSet,
    base_name='locations',
)
router.register(
    r'years/(?P<year>[0-9]{4})/rules',
    rules.RulesViewSet,
    base_name='rules',
)
router.register(
    r'years/(?P<year>[0-9]{4})/performers',
    performers.PerformerViewSet,
    base_name='performers',
)
router.register(
    r'years/(?P<year>[0-9]{4})/schedule',
    schedule.ScheduleEventViewSet,
    base_name='schedule',
)
router.register(r'accomodations', accomodations.AccomodationViewSet)
