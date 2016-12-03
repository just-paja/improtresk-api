"""Common items for all e-mails."""

WORKSHOP = "{lectorName}: {name}"

WORKSHOP_LIST_ITEM = """
    {order}. {lectorName}: {name}
"""

PAYMENT = """
    Částka: {amount} Kč
    Číslo účtu: {senderAccount}/{senderBank}
    Variabilní symbol: {symvar}
    Přijato bankou: {received}
    Zpracováno: {updatedAt}
"""

ACCOUNT_INFO = """
Účet: 2800754192/2010
Částka: {price}
Variabilní symbol: {symvar}
"""

MAIL_FOOTER = """
Organizační tým Improtřesku {year}
http://improtresk.cz
info@improtresk.cz

--

Tato zpráva byla vyžádána v rámci placené přihlášky na Improtřesk {year}.
"""


def formatWorkshop(data):
    """Format workshop data into string."""
    print("%s" % data)
    return WORKSHOP.format(data)


def formatWorkshopListItem(data):
    """Format workshop data into list item string."""
    return WORKSHOP_LIST_ITEM.format(data)


def formatWorkshopList(workshops):
    """Format workshop list data into string."""
    return "\n".join(map(formatWorkshopListItem, workshops))


def formatMail(template, data):
    """Format e-mail body to be sent."""
    body = template + MAIL_FOOTER
    return body.format(data)
