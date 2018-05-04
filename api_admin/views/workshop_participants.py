from api.models import Order, Year
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render


@staff_member_required
def workshop_participants(request, festivalId):
    festival = Year.objects.get(pk=festivalId)
    workshops = festival.get_workshops()
    workshopless = Order.objects.filter(
        paid=True,
        canceled=False,
        year=festivalId,
        reservation__workshop_price=None,
    )
    data = []
    for workshop in workshops:
        data.append({
            'name': workshop.name,
            'participants': [
                participant.participant for participant in workshop.participants.all()
            ],
        })

    if workshopless.count() > 0:
        workshopless_data = {
            'name': 'Bez Workshopu',
            'participants': []
        }
        data.append(workshopless_data)
        for order in workshopless:
            workshopless_data['participants'].append(order.participant)
    return render(
        request,
        'stats/workshop_participants.html',
        {
            'festival': festival,
            'workshops': data,
        },
    )
