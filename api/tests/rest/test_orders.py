"""Tests for orders rest endpoint."""

import json

from api.rest.orders import OrderViewSet

from django.test import TestCase
from django.urls import reverse

from model_mommy import mommy

from rest_framework.test import APIRequestFactory, force_authenticate


class OrdersEndpointTest(TestCase):
    """Test accomodation methods."""

    def setUp(self):
        self.factory = APIRequestFactory()
        self.default_user = mommy.make('api.Participant')
        self.order = mommy.make(
            'api.Order',
            participant=self.default_user,
        )
        self.price_level = mommy.make('api.PriceLevel')
        self.workshop = mommy.make('api.Workshop')
        self.price = mommy.make(
            'api.WorkshopPrice',
            price_level=self.price_level,
            workshop=self.workshop,
        )
        self.reservation = mommy.make(
            'api.Reservation',
            order=self.order,
            workshop_price=self.price,
        )
        self.view = OrderViewSet.as_view(
            actions={
                'get': 'retrieve',
                'delete': 'destroy',
                'patch': 'update',
            },
        )

    def test_order_update_missing_order(self):
        request = self.factory.patch(
            reverse('order-detail', args=[356568]),
            json.dumps({'workshop': self.workshop.pk}),
            content_type='application/json',
        )
        force_authenticate(request, user=self.default_user)
        response = self.view(request, pk=356568).render()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            json.loads(response.content.decode('utf-8')),
            {'errors': ['unknown-object']},
        )

    def test_order_update_missing_workshop(self):
        request = self.factory.patch(
            reverse('order-detail', args=[self.order.pk]),
            json.dumps({'workshop': 335757}),
            content_type='application/json',
        )
        force_authenticate(request, user=self.default_user)
        response = self.view(request, pk=self.order.pk)
        self.assertEqual(response.status_code, 404)

    def test_order_update_not_owned_order(self):
        invalid_user = mommy.make('api.Participant')
        request = self.factory.patch(
            reverse('order-detail', args=[self.order.pk]),
            json.dumps({'workshop': self.workshop.pk}),
            content_type='application/json',
        )
        force_authenticate(request, user=invalid_user)
        response = self.view(request, pk=self.order.pk).render()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            json.loads(response.content.decode('utf-8')),
            {'errors': ['must-be-owner']},
        )

    def test_order_update_no_reservation(self):
        order = mommy.make(
            'api.Order',
            participant=self.default_user,
        )
        request = self.factory.patch(
            reverse('order-detail', args=[order.pk]),
            json.dumps({'workshop': self.workshop.pk}),
            content_type='application/json',
        )
        force_authenticate(request, user=self.default_user)
        response = self.view(request, pk=order.pk).render()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            json.loads(response.content.decode('utf-8')),
            {'errors': ['make-reservation-first']},
        )

    def test_order_update_no_workshop_price(self):
        order = mommy.make(
            'api.Order',
            participant=self.default_user,
            reservation=mommy.make('api.Reservation'),
        )
        request = self.factory.patch(
            reverse('order-detail', args=[order.pk]),
            json.dumps({'workshop': self.workshop.pk}),
            content_type='application/json',
        )
        force_authenticate(request, user=self.default_user)
        response = self.view(request, pk=order.pk).render()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            json.loads(response.content.decode('utf-8')),
            {'errors': ['make-reservation-first']},
        )

    def test_order_update_price_level_mismatch(self):
        order = mommy.make(
            'api.Order',
            participant=self.default_user,
        )
        mommy.make(
            'api.Reservation',
            order=order,
            workshop_price=mommy.make(
                'api.WorkshopPrice',
                price_level=mommy.make('api.PriceLevel'),
            ),
        )

        request = self.factory.patch(
            reverse('order-detail', args=[order.pk]),
            json.dumps({'workshop': self.workshop.pk}),
            content_type='application/json',
        )
        force_authenticate(request, user=self.default_user)
        response = self.view(request, pk=order.pk).render()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            json.loads(response.content.decode('utf-8')),
            {'errors': ['no-matching-price-level']},
        )

    def test_order_update_no_change(self):
        request = self.factory.patch(
            reverse('order-detail', args=[self.order.pk]),
            json.dumps({'workshop': self.workshop.pk}),
            content_type='application/json',
        )
        force_authenticate(request, user=self.default_user)
        response = self.view(request, pk=self.order.pk).render()
        self.assertEqual(response.status_code, 204)

    def test_order_update_no_reassignment(self):
        workshop = mommy.make('Workshop')
        price = mommy.make(
            'api.WorkshopPrice',
            price_level=self.price_level,
            workshop=workshop,
        )

        request = self.factory.patch(
            reverse('order-detail', args=[self.order.pk]),
            json.dumps({'workshop': workshop.pk}),
            content_type='application/json',
        )
        force_authenticate(request, user=self.default_user)
        response = self.view(request, pk=self.order.pk).render()
        self.assertEqual(response.status_code, 204)
        self.order.reservation.refresh_from_db()
        self.assertEqual(self.order.reservation.workshop_price.pk, price.pk)
        self.assertEqual(self.default_user.assigned_workshop, None)

    def test_order_update_reassignment(self):
        workshop = mommy.make('Workshop')
        price = mommy.make(
            'api.WorkshopPrice',
            price_level=self.price_level,
            workshop=workshop,
        )
        self.default_user.assigned_workshop = self.workshop
        self.default_user.save()

        request = self.factory.patch(
            reverse('order-detail', args=[self.order.pk]),
            json.dumps({'workshop': workshop.pk}),
            content_type='application/json',
        )
        force_authenticate(request, user=self.default_user)
        response = self.view(request, pk=self.order.pk).render()
        self.assertEqual(response.status_code, 204)
        self.order.reservation.refresh_from_db()
        self.default_user.refresh_from_db()
        self.assertEqual(self.order.reservation.workshop_price.pk, price.pk)
        self.assertEqual(self.default_user.assigned_workshop.pk, workshop.pk)
