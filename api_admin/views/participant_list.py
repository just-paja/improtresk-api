from api.models import Participant, Reservation
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from django.shortcuts import render


def get_participant_reservation(order):
    if order:
        return Reservation.objects.filter(
            order=order,
        ).first()
    return None


@staff_member_required
def participant_list(request, festivalId):
    participants = Participant.objects\
        .filter(orders__year=festivalId)\
        .order_by('name')\
        .all()
    data = []

    for participant in participants:
        order = participant.orders.filter(
            paid=True,
            year=festivalId,
            confirmed=True,
            canceled=False,
        )
        reservation = get_participant_reservation(order)
        payment_sum = 0
        if order.payments.count() > 0:
            payment_sum = order.payments.aggregate(paid=Sum('amount')).get('paid')
        if order and reservation:
            accomodation = reservation.accomodation
            meal_reservations = reservation.mealreservation_set.all()

            data.append({
                'name': participant.name,
                'email': participant.email,
                'workshop': participant.assigned_workshop.name,
                'accomodation': accomodation.name,
                'meals': meal_reservations,
                'cash_expected': order.price,
                'cash_received': payment_sum,
            })

    return render(
        request,
        'stats/participant_list.html',
        {
            'data': data,
        },
    )
