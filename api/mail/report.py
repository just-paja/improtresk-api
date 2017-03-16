"""Common items for all e-mails."""

ASSIGNMENT_FAILED_SUBJECT = """[O{order}]: Nepovedlo se zařadit na workshop"""
ASSIGNMENT_FAILED_BODY = """
Přihlášku se nepovedlo zařadit na workshop kvůli nejasnému\
výsledku. Buď je cílový workshop plný a nebo ostatní přihlášky\
nemají kam se zařadit.

ID Objednávky: {order}
Účastník: {participant}
Cílový workshop: {workshop}
"""
