from api.models import Order, Year
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render


@staff_member_required
def workshop_capacity(request, festivalId):
    festival = Year.objects.get(pk=festivalId)
    workshops = festival.get_workshops()

    for workshop in workshops:
        workshop.assignment_count = workshop.participants.count()
        workshop.assignment_list = workshop.participants.all()

        for assignment in workshop.assignment_list:
            assignment.order = Order.objects.filter(
                participant=assignment.participant,
                reservation__workshop_price__workshop=workshop,
                confirmed=True,
                canceled=False,
            ).first()

    return render(
        request,
        'stats/workshops.html',
        {
            'festival': festival,
            'workshops': workshops,
        },
    )
