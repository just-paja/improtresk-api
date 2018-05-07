from api.models import Order, Payment, Year
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from ..models import Checkin


@staff_member_required
def checkin(request, code):
    year = Year.objects.get_current()
    if not year.current:
        raise Http404
    order = get_object_or_404(Order, pk=code)
    reservation = order.reservation
    checked_in = Checkin.objects.filter(order=order).first()
    overpaid_by = 0
    paid_price = Payment.objects.filter(
        order=order,
    ).aggregate(amount=Sum('amount')).get('amount')
    print(paid_price)

    if paid_price is not None:
        overpaid_by = paid_price - order.price
    return render(request, 'checkin/index.html', {
        'accomodation': reservation.accomodation,
        'checked_in': checked_in,
        'meals': reservation.meals.all(),
        'order': order,
        'overpaid_by': overpaid_by,
        'participant': order.participant,
        'workshop': reservation.workshop,
        'year': year,
        'paid_price': paid_price,
    })
