"""Site administration module."""
from django.contrib import admin
from django.urls import reverse

DEFAULT_READONLY = ['created_at', 'updated_at']


class BaseAdminModel(admin.ModelAdmin):
    """Base admin for models."""

    def get_readonly_fields(self, request, obj=None):
        """Define default readonly fields."""
        return DEFAULT_READONLY + list(self.readonly_fields)

    def changelist_view(self, request, *args, **kwargs):
        from django.http import HttpResponseRedirect
        if hasattr(self, 'default_filters') and self.default_filters:
            if len(request.GET) == 0:
                print(self.opts)
                url = reverse('admin:%s_%s_changelist' % (
                    self.opts.app_label,
                    'accomodation'
                ))
                filters = []
                for filter in self.default_filters:
                    print(filter)
                    key = filter.split('=')[0]
                    if key not in request.GET:
                        filters.append(filter)
                if filters:
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
