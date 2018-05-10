from api.models import Accomodation, Participant, Year

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Count


@staff_member_required
def accomodation_inhabitant_list(request, festivalId):
    festival = Year.objects.get(pk=festivalId)
    accomodations = Accomodation.objects\
        .filter(year=festivalId)\
        .order_by('name')\
        .all()
    data = []

    for accomodation in accomodations:
        rooms = accomodation.rooms.order_by('number').all()
        data_accomodation = {
            'name': accomodation.name,
            'rooms': [],
            'without_room': [],
        }
        data.append(data_accomodation)
        for room in rooms:
            data_room = {
                'number': room.number,
                'size': room.size,
                'inhabitants': [
                    inhabitant.participant
                    for inhabitant in room.inhabitants.all()
                ],
            }
            data_accomodation['rooms'].append(data_room)
        without_room = Participant.objects.filter_by_festival(festivalId).filter(
            orders__reservation__accomodation=accomodation,
        ).annotate(room_count=Count('inhabited_rooms')).filter(room_count=0)
        data_accomodation['without_room'] = without_room.all()
    print(data)
    return render(request, 'stats/accomodation_inhabitants.html', {
        'data': data,
        'festival': festival,
    })
