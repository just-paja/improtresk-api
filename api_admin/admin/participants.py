from django.contrib.admin import SimpleListFilter

from api.models import Participant, ParticipantStay, ParticipantWorkshop, Year

from ..models import BaseAdminModel, BaseInlineAdminModel


class ParticipantYearFilter(SimpleListFilter):
    title = 'Year Participation'
    parameter_name = 'year__id__exact'

    def lookups(self, request, model_admin):
        return [(year.id, year.year) for year in Year.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter_by_festival(self.value())


class ParticipantMealFilter(SimpleListFilter):
    title = 'Meal'
    parameter_name = 'has_meal'

    def lookups(self, request, model_admin):
        return [(1, 'Yes'), (2, 'No')]

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter_with_meal()
        if self.value() == '2':
            return queryset.filter_without_meal()


class ParticipantWorkshopFilter(SimpleListFilter):
    title = 'Workshop'
    parameter_name = 'on_workshop'

    def lookups(self, request, model_admin):
        return [(1, 'Yes'), (2, 'No')]

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter_with_workshop()
        if self.value() == '2':
            return queryset.filter_without_workshop()


class ParticipantStayAdmin(BaseInlineAdminModel):
    """Admin model for Participant workshop assignment."""

    model = ParticipantStay
    exclude = ['created_at']


class ParticipantWorkshopAdmin(BaseInlineAdminModel):
    """Admin model for Participant workshop assignment."""

    model = ParticipantWorkshop
    exclude = ['created_at']


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
    autocomplete_fields = ['team']
    list_filter = (
        ParticipantYearFilter,
        ParticipantWorkshopFilter,
        ParticipantMealFilter,
        'team',
        'newsletter',
    )
    search_fields = ['name', 'email']


class TeamAdmin(BaseAdminModel):
    """Admin model for Teams."""

    list_display = (
        'id',
        'name',
        'visibility',
        'desc',
    )

    search_fields = ('name',)
