"""E-mail templates for signups."""

ORDER_CONFIRMED_SUBJECT = "Tvoje přihláška"
ORDER_CONFIRMED_BODY = """Ahoj,

Přijali jsme tvojí přihlášku. Na workshop tě však zařadíme až v \
momentě kdy bude zaplacena. Rezervujeme ti místo na workshopu do \
{validUntil:{datetime_format}}, pokud nám od tebe nepřijde platba včas, \
tak tvoje místo na workshopu nabídneme ostatním.

O zařazení na workshop a potvrzení platby ti přijde oznámení e-mailem.

Detaily platby:
{accountInfo}

Objednaný workshop: {workshop}
Čas propadnutí rezervace: {validUntil:{datetime_format}}

    -----

Kdyby došlo k jakékoliv nesrovnalosti, neváhej nás prosím okamžitě kontaktovat.
"""


ORDER_PAID_SUBJECT = "Přihláška zaplacena"
ORDER_PAID_BODY = """Hurá!

Tvoje přihláška je zaplacena. V tento okamžik jsi byl(a) zařazen(a) \
do fronty na workshop podle tvých preferencí. Zařazování na workshopy \
probíhá částečně manuálně a částečně automaticky - někde u počítače sedí \
člověk, který potvrzuje kdo kam půjde podle toho kdo dřív zaplatil. \
Může to tedy chvíli trvat. Jakmile tě zařadíme, okamžitě se ti ozveme.

Workshop: {workshop}
Celkem zaplaceno: {amountPaid} Kč

Spárované platby:
{payments}

    -----

Kdyby došlo k jakékoliv nesrovnalosti, neváhej nás prosím okamžitě kontaktovat.
"""

ORDER_UPDATE_SUBJECT = "Aktualizace stavu přihlášky"
ORDER_UPDATE_BODY = """Ahoj,

posíláme ti aktualizaci tvojí přihlášky na Improtřesk {year}.

Přihláška stále není zaplacena, chybí nám od tebe {amountLeft} Kč. \
Pošli je prosím na náš účet bankovním převodem.

Workshop: {workshop}
{accountInfo}

Celkem zaplaceno: {amountPaid} Kč

Spárované platby:
{payments}

    -----

Kdyby došlo k jakékoliv nesrovnalosti, neváhej nás prosím okamžitě kontaktovat.
"""

ASSIGNED_SUBJECT = "Zařazení na workshop"
ASSIGNED_BODY = """
Ahoj,

na základě preferencí v tvojí přihlášce jsme tě zařadili na tento workshop:
{currentWorkshop}

Kdyby došlo k jakékoliv nesrovnalosti, neváhej nás prosím okamžitě kontaktovat.
"""

REASSIGNED_SUBJECT = "Přeřazení na jiný workshop"
REASSIGNED_BODY = """
Ahoj,

přeřadili jsme tě na jiný workshop.

{prevWorkshop} -> {currentWorkshop}

Kdyby došlo k jakékoliv nesrovnalosti, neváhej nás prosím okamžitě kontaktovat.
"""

REMOVED_SUBJECT = "Odhlášení z workshopu"
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
