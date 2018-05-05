from datetime import datetime

from api.models import Order, Participant, ParticipantWorkshop, Payment, Year
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum
from django.shortcuts import render


def get_festival_orders(festival):
    return Order.objects.filter(year=festival)


def get_festival_participants(festival):
    return Participant.objects.filter(
        orders__year=festival,
        orders__paid=True,
        orders__canceled=False,
    )


def get_festival_payments(festival):
    return Payment.objects.filter(order__year=festival)


def get_workshop_participants_count(festival):
    return ParticipantWorkshop.objects.filter(
        year=festival,
    ).count()


def get_workshopless_participants_count(festival):
    return get_festival_orders(festival).filter(
        reservation__workshop_price=None,
        paid=True,
        canceled=False,
    ).count()


def get_team_participants_count(festival):
    return get_festival_participants(festival).exclude(team=None).count()


def get_teamless_participants_count(festival):
    return get_festival_participants(festival).filter(team=None).count()


def get_lunch_participants_count(festival):
    return get_festival_participants(festival).annotate(
        meals_count=Count('orders__reservation__meals'),
    ).filter(meals_count__gt=0).count()


def get_lunchless_participants_count(festival):
    return get_festival_participants(festival).annotate(
        meals_count=Count('orders__reservation__meals'),
    ).filter(meals_count=0).count()


def get_orders_count(festival):
    return get_festival_orders(festival).count()


def get_paid_orders_count(festival):
    return get_festival_orders(festival).filter(canceled=False, paid=True).count()


def get_unpaid_confirmed_orders_count(festival):
    return get_festival_orders(festival).filter(
        canceled=False,
        confirmed=True,
        paid=False,
    ).count()


def get_unpaid_unconfirmed_orders_count(festival):
    return get_festival_orders(festival).filter(
        canceled=False,
        confirmed=False,
        paid=False,
    ).count()


def get_canceled_orders_count(festival):
    return get_festival_orders(festival).filter(canceled=True).count()


def get_amount_received(festival):
    return get_festival_payments(festival).aggregate(Sum('amount'))


def get_amount_expected(festival):
    return get_festival_orders(festival).filter(
        canceled=False,
        confirmed=True,
        reservation__ends_at__gt=datetime.now(),
    ).aggregate(Sum('price'))


def get_paired_payments_count(festival):
    return get_festival_payments(festival).count()


def get_festival_stats(festival):
    return {
        'orders_total': get_orders_count(festival),
        'orders_paid_active': get_paid_orders_count(festival),
        'orders_unpaid_confirmed': get_unpaid_confirmed_orders_count(festival),
        'orders_unpaid_unconfirmed': get_unpaid_unconfirmed_orders_count(festival),
        'orders_canceled': get_canceled_orders_count(festival),
        'participants_on_workshop': get_workshop_participants_count(festival),
        'participants_without_workshop': get_workshopless_participants_count(festival),
        'participants_with_team': get_team_participants_count(festival),
        'participants_without_team': get_teamless_participants_count(festival),
        'participants_with_lunch': get_lunch_participants_count(festival),
        'participants_without_lunch': get_lunchless_participants_count(festival),
        'payments_paired_total': get_paired_payments_count(festival),
        'amount_received': get_amount_received(festival).get('amount__sum') or 0,
        'amount_expected': get_amount_expected(festival).get('price__sum') or 0,
    }


@staff_member_required
def numbers(request, festivalId):
    festival = Year.objects.get(pk=festivalId)
    return render(request, 'stats/numbers.html', {
        'festival': festival,
        'stats': get_festival_stats(festival),
    })
