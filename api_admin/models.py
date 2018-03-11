"""Site administration module."""
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse

from api import models as models_api

DEFAULT_READONLY = ['created_at', 'updated_at']


class BaseAdminModel(admin.ModelAdmin):
    """Base admin for models."""

    def get_readonly_fields(self, request, obj=None):
        """Define default readonly fields."""
        return DEFAULT_READONLY + list(self.readonly_fields)

    def changelist_view(self, request, *args, **kwargs):
        referer = request.META.get('HTTP_REFERER', None)
        filters = []

        url = reverse('admin:%s_%s_changelist' % (
            self.opts.app_label,
            'accomodation'
        ))
        if 'year' in self.list_filter:
            currentYear = (
                models_api.Year.objects
                    .filter(current=True)
                    .order_by('-year')
                    .first()
            )
            if currentYear:
                filters.append('year__id__exact=%s' % currentYear.id)
        if filters and len(request.GET) == 0:
            return HttpResponseRedirect("%s?%s" % (url, "&".join(filters)))
        return super(BaseAdminModel, self).changelist_view(request, *args, **kwargs)


class BaseInlineAdminModel(admin.TabularInline):
    """Base admin for Inline models."""
    extra = 1

    def get_readonly_fields(self, request, obj=None):
        """Define default readonly fields."""
        return DEFAULT_READONLY + list(self.readonly_fields)


class BaseTextAdminModel(BaseAdminModel):
    """Base admin for Text models."""

    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'lang', 'updated_at')
    list_filter = ('lang',)
    fields = [
        'name',
        'slug',
        'lang',
        'category',
        'text',
    ]


class BaseTagAdmin(BaseAdminModel):
    """Admin model for tag-like models."""

    prepopulated_fields = {'slug': ('name',)}


class FoodAdminMixin():
    list_display = (
        'name',
        'meal',
        'capacity',
        'created_at',
        'visibility',
    )
