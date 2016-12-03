"""E-mail templates for signups."""

CONFIRMATION_SUBJECT = "Potvrzení přihlášky"
CONFIRMATION_BODY = """Ahoj,

přijali jsme tvojí přihlášku na Improtřesk {year}. Zde je rekapitulace:

Jméno: {name}
Telefon: {phone}
E-mail: {email}
Způsob platby: {paymentMethod}

Workshopy:
{workshops}

{accountInfo}

Po uhrazení účastnického poplatku budete přiřazen na workshop. O přijetí \
platby tě budeme informovat automatickým e-mailem. Detaily platby jsou níže.

Do zprávy prosím uveď pro kontrolu svoje jméno.

{footer}
"""


ORDER_PAID_SUBJECT = "Přihláška zaplacena"
ORDER_PAID_BODY = """
Hurá, tvoje přihláška je zaplacena. V tento okamžik jsi byl(a) zařazen(a) \
do fronty na workshop podle tvých preferencí. Zařazování na workshopy \
probíhá částečně manuálně a částečně automaticky - někde u počítače sedí \
člověk, který potvrzuje kdo kam půjde podle toho kdo dřív zaplatil. \
Může to tedy chvíli trvat. Jakmile tě zařadíme, okamžitě se ti ozveme.

Celkem zaplaceno: {paidAmmount} Kč

Spárované platby:
    {payments}

    -----

Kdyby došlo k jakékoliv nesrovnalosti, neváhej nás prosím okamžitě kontaktovat.
"""

ORDER_UPDATE_NOT_PAID_SUBJECT = "Aktualizace stavu přihlášky"
ORDER_UPDATE_NOT_PAID_BODY = """
Ahoj,

dorazila nám na účet od tebe platba. Posíláme ti touto cestou aktualizaci \
tvojí přihlášky na Improtřesk {year}.

Přihláška stále není zaplacena, chybí nám od tebe {missingAmount} Kč. \
Pošli je prosím na náš účet bankovním převodem.

{accountInfo}

Celkem zaplaceno: {paidAmmount} Kč

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

Tvoje preference z přihlášky:

{workshopPreferences}

Kdyby došlo k jakékoliv nesrovnalosti, neváhej nás prosím okamžitě kontaktovat.
"""

REASSIGNED_SUBJECT = "Přeřazení na jiný workshop"
REASSIGNED_BODY = """
Ahoj,

přeřadili jsme tě na jiný workshop.

{prevWorkshop} -> {currentWorkshop}

Tvoje preference z přihlášky:

{workshopPreferences}

Kdyby došlo k jakékoliv nesrovnalosti, neváhej nás prosím okamžitě kontaktovat.
"""

REMOVED_SUBJECT = "Odhlášení z workshopu"
REMOVED_BODY = """
Ahoj,

vyřadili jsme tě z workshopu {prevWorkshop}.

Kdyby došlo k jakékoliv nesrovnalosti, neváhej nás prosím okamžitě kontaktovat.
"""
