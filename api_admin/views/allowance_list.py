from api.models import Order, Year
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render


@staff_member_required
def allowance_list(request, festivalId):
    festival = Year.objects.get(pk=festivalId)
    orders = Order.objects\
        .filter(
            year=festivalId,
            canceled=False,
            confirmed=True,
            paid=True,
        )\
        .exclude(price=0)\
        .order_by('participant__name')\
        .all()
    data = []

    for order in orders:
        data.append({
            'name': order.participant.name,
            'email': order.participant.email,
            'address': order.participant.address,
            'cash_expected': order.price,
        })

    return render(request, 'stats/allowance_list.html', {
        'data': data,
        'festival': festival,
    })
