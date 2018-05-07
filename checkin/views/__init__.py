from api.models import Order, Payment, Year
from api.models.payment import STATUS_PAID
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from functools import wraps

from ..models import Checkin


def has_food_selected(mealreservations):
    for meal in mealreservations:
        if not meal.soup or not meal.food:
            return False
    return True


def is_overpaid(order, paid_price):
    diff = paid_price - order.price
    return diff < 0 or order.over_paid


def is_accomodation_selected(reservation, accomodation_room):
    if not has_accomodation_rooms(reservation.accomodation) or (
        accomodation_room
    ):
        return True
    return False


def has_accomodation_rooms(accomodation):
    return accomodation.rooms.count() > 0


def require_checkin_data(func):
    @wraps(func)
    def func_wrapper(request, code, *args, **kwargs):
        year = Year.objects.get_current()
        if not year.current:
            raise Http404
        try:
            order = Order.objects.filter_by_code(code).get()
        except Order.DoesNotExist:
            raise Http404
        reservation = order.reservation
        checked_in = Checkin.objects.filter(order=order).first()
        paid_price = Payment.objects.filter(
            order=order,
        ).aggregate(amount=Sum('amount')).get('amount')
        if paid_price is None:
            paid_price = 0
        mealreservations = reservation.mealreservation_set.all()
        paid_diff = order.price - paid_price
        food_selected = has_food_selected(mealreservations)
        rooms = order.participant.inhabited_rooms.filter(
            room__accomodation=reservation.accomodation,
        )
        accomodation_room = rooms.first()
        accomodation_room_selected = is_accomodation_selected(reservation, accomodation_room)
        can_checkin = (
            food_selected and
            accomodation_room_selected and
            not is_overpaid(order, paid_price)
        )
        return func(request, code=code, checkin={
            'accomodation_has_rooms': has_accomodation_rooms(reservation.accomodation),
            'accomodation_room_selected': accomodation_room_selected,
            'accomodation_room': accomodation_room,
            'accomodation': reservation.accomodation,
            'can_checkin': can_checkin,
            'code': code,
            'food_selected': food_selected,
            'checked_in': checked_in,
            'just_checked_in': 'checkedIn' in request.GET,
            'just_paid': 'paid' in request.GET,
            'just_refunded': 'refunded' in request.GET,
            'meals': mealreservations,
            'order': order,
            'paid_diff': paid_diff,
            'paid_price': paid_price,
            'participant': order.participant,
            'workshop': reservation.workshop,
            'year': year,
        }, *args, **kwargs)
    return func_wrapper


@require_http_methods(['GET'])
@staff_member_required
@require_checkin_data
def participant_checkin(request, code, checkin):
    return render(request, 'checkin/index.html', checkin)


@require_http_methods(['POST'])
@staff_member_required
@require_checkin_data
def participant_paid(request, code, checkin):
    query = None
    if checkin.get('paid_diff') > 0:
        order = checkin.get('order')
        payment = Payment(
            order=order,
            amount=checkin.get('paid_diff'),
            ident="%s:%s" % (order.symvar, timezone.now()),
            message='Paid by cash',
            status=STATUS_PAID,
            symvar=order.symvar,
        )
        payment.save()
        query = '?paid'
    return redirect("%s%s" % (reverse(participant_checkin, kwargs={'code': code}), query))


@require_http_methods(['POST'])
@staff_member_required
@require_checkin_data
def participant_refunded(request, code, checkin):
    query = None
    if checkin.get('paid_diff') < 0:
        order = checkin.get('order')
        payment = Payment(
            order=order,
            amount=checkin.get('paid_diff'),
            ident="%s:%s" % (order.symvar, timezone.now()),
            message='Refunded by cash',
            status=STATUS_PAID,
            symvar=order.symvar,
        )
        payment.save()
        query = '?refunded'
    return redirect("%s%s" % (reverse(participant_checkin, kwargs={'code': code}), query))


@require_http_methods(['POST'])
@staff_member_required
@require_checkin_data
def participant_check(request, code, checkin):
    query = None
    if not checkin.get('checkin', False):
        check = Checkin(order=checkin.get('order'))
        check.save()
        query = '?checkedIn'
    return redirect("%s%s" % (reverse(participant_checkin, kwargs={'code': code}), query))
