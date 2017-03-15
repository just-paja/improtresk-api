"""Common items for all e-mails."""

from django.conf import settings

format_config = {
    'year': settings.YEAR,
    'datetime_format': '%-d. %-m. %Y %H:%M:%S',
}

WORKSHOP = "{name}"

WORKSHOP_LIST_ITEM = """
    {order}. {lectorName}: {name}
"""

PAYMENT = """
    Částka: {amount} Kč
    Odesláno z účtu: {sender}/{bank}
    Variabilní symbol: {symvar}
    Přijato bankou: {received_at:{datetime_format}}
    Zpracováno: {created_at:{datetime_format}}"""

ACCOUNT_INFO = """
Číslo účtu: 2800754192/2010
Částka k zaplacení: {price} Kč
Variabilní symbol: {symvar}"""

MAIL_FOOTER = """
Organizační tým Improtřesku
http://improtresk.cz
info@improtresk.cz

--

Tato zpráva byla vyžádána v rámci placené přihlášky na Improtřesk {year}.
"""


def formatAccountInfo(data):
    """Format workshop data into string."""
    return ACCOUNT_INFO.format(**{**data, **format_config})


def formatPayment(data):
    """Format workshop data into string."""
    return PAYMENT.format(**{**data, **format_config})


def formatPayments(payments):
    """Format workshop data into string."""
    return "\n".join(map(formatPayment, payments))


def formatWorkshop(data):
    """Format workshop data into string."""
    return WORKSHOP.format(**{**data, **format_config})


def formatWorkshopListItem(data):
    """Format workshop data into list item string."""
    return WORKSHOP_LIST_ITEM.format(**{**data, **format_config})


def formatWorkshopList(workshops):
    """Format workshop list data into string."""
    return "\n".join(map(formatWorkshopListItem, workshops))


def formatMail(template, data):
    """Format e-mail body to be sent."""
    body = template + MAIL_FOOTER
    return body.format(**{**data, **format_config})
