from rest_framework import routers

from api.rest import accomodations, lector_roles, lectors, rules, workshops,\
    workshop_difficulties, years
from api_textual.rest import news, texts, workshop_locations

router = routers.DefaultRouter()
router.register(r'lectorRoles', lector_roles.LectorRoleViewSet)
router.register(r'lectors', lectors.LectorViewSet)
router.register(r'news', news.NewsViewSet)
router.register(r'texts', texts.TextViewSet)
router.register(r'workshopDifficulties', workshop_difficulties.WorkshopDifficultyViewSet)
router.register(r'years', years.YearViewSet)
router.register(
    r'years/(?P<year>[0-9]{4})/workshops',
    workshops.WorkshopViewSet,
    base_name='workshops',
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
router.register(r'accomodations', accomodations.AccomodationViewSet)
