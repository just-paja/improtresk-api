from api import models as models_api

from ..models import BaseAdminModel, BaseInlineAdminModel


class ParticipantStayAdmin(BaseInlineAdminModel):
    """Admin model for Participant workshop assignment."""

    model = models_api.ParticipantStay
    exclude = [
        'created_at',
    ]


class ParticipantWorkshopAdmin(BaseInlineAdminModel):
    """Admin model for Participant workshop assignment."""

    model = models_api.ParticipantWorkshop
    exclude = [
        'created_at',
    ]


class ParticipantAdmin(BaseAdminModel):
    """Admin model for Participants."""

    inlines = [
        ParticipantWorkshopAdmin,
        ParticipantStayAdmin,
    ]
    readonly_fields = [
        'password',
        'last_login',
    ]
    exclude = [
        'is_superuser',
        'groups',
        'user_permissions',
        'first_name',
        'last_name',
        'is_staff',
        'is_active',
        'assigned_workshop',
    ]
    list_display = (
        'name',
        'team',
        'email',
        'newsletter',
        'created_at',
    )
    list_filter = ('team', 'newsletter')
    search_fields = ['name', 'email']


class TeamAdmin(BaseAdminModel):
    """Admin model for Teams."""

    list_display = (
        'id',
        'name',
        'visibility',
        'desc',
    )
