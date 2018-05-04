from api.models import Accomodation, Participant, Year
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render


@staff_member_required
def accomodation_inhabitant_list(request, festivalId):
    festival = Year.objects.get(pk=festivalId)
    accomodations = Accomodation.objects\
        .filter(
            year=festivalId,
            requires_identification=True,
        )\
        .order_by('name')\
        .all()
    data = []

    for accomodation in accomodations:
        data.append({
            'name': accomodation.name,
            'address': accomodation.address,
            'participants': Participant.objects.filter(
                orders__year=festivalId,
                orders__canceled=False,
                orders__paid=True,
                orders__confirmed=True,
                orders__reservation__accomodation=accomodation,
            ).all()
        })

    return render(request, 'stats/accomodation_inhabitants.html', {
        'data': data,
        'festival': festival,
    })
