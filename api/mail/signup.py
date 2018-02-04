"""E-mail templates for signups."""


REMOVED_BODY = """Ahoj,

vyřadili jsme tě z workshopu {prevWorkshop}.

Kdyby došlo k jakékoliv nesrovnalosti, neváhej nás prosím okamžitě kontaktovat.
"""

PASSWORD_RESET_REQUEST_SUBJECT = "Změna hesla"
PASSWORD_RESET_REQUEST_BODY = """Ahoj,

dostali jsme žádost na obnovu hesla k tvému účtu na Improtřesk. Pro zadání \
nového hesla následuj následující odkaz:

http://improtresk.cz/nove-heslo?token={token}

    -----

Pokud jsi o změnu hesla nepožádal, tak tento e-mail ignoruj.
"""
