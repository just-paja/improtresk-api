from django.template.defaultfilters import escape
from django.utils.html import format_html
from django.urls import reverse

VISIBILITY_PRIVATE = 1
VISIBILITY_PUBLIC = 2
VISIBILITY_DELETED = 3

VISIBILITY_CHOICES = (
    (VISIBILITY_PRIVATE, 'Private'),
    (VISIBILITY_PUBLIC, 'Public'),
    (VISIBILITY_DELETED, 'Deleted'),
)


def format_relation_link(model_ident, pk, label):
    return format_html(
        '<a href="{}">{}</a>',
        reverse("admin:%s_change" % model_ident, args=(pk,)),
        escape(label)
    )


def format_checkin_link(code):
    return format_html(
        '<a href="{}">{}</a>',
        reverse("checkin", kwargs={'code': code}),
        escape(code)
    )
