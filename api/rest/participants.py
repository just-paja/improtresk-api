from datetime import date

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import Http404
from django.utils.timezone import localtime, now

from rest_framework import mixins, permissions, serializers, status, viewsets

from rest_framework.response import Response

from rest_framework_extensions.mixins import NestedViewSetMixin

from ..models import Participant
from ..models.participantToken import PASSWORD_RESET


def is_true(value):
    if not value:
        raise serializers.ValidationError('Rules must be accepted')


def is_eighteen(value):
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))

    if age < 18:
        raise serializers.ValidationError('Must be older than 18 years')


def is_email_unique(value):
    participant_exists = Participant.objects.filter(email=value)
    user_exists = User.objects.filter(email=value)
    if participant_exists or user_exists:
        raise ValidationError("Email address already exists, must be unique")


class ParticipantSerializer(serializers.HyperlinkedModelSerializer):
    team_name = serializers.CharField(
        write_only=True,
        allow_blank=True,
    )
    team = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='name',
    )
    assigned_workshop = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='id',
    )
    birthday = serializers.DateField(
        validators=[is_eighteen],
    )
    rules_accepted = serializers.BooleanField(
        validators=[is_true],
    )
    email = serializers.EmailField(
        validators=[is_email_unique],
    )

    class Meta:
        model = Participant
        fields = (
            'id',
            'name',
            'address',
            'password',
            'team_name',
            'team',
            'email',
            'phone',
            'birthday',
            'rules_accepted',
            'newsletter',
            'assigned_workshop',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        validated_data['username'] = validated_data['email']
        participant = super().create(validated_data)
        participant.set_password(validated_data['password'])
        participant.save()
        return participant


class ParticipantPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ('password',)
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class ParticipantViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = [permissions.IsAdminUser]


class RegistrationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer


class WhoAmIViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Participant.objects
    serializer_class = ParticipantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        serializer = self.get_serializer(request.user.participant)
        return Response(serializer.data)


class ResetPasswordViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Participant.objects

    def create(self, request, *args, **kwargs):
        user = self.queryset\
            .filter(email=request.data.get('email', None))\
            .first()

        if user:
            user.request_password_reset()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            {'email': 'Tento e-mail nepoznáváme'},
            status=status.HTTP_404_NOT_FOUND,
        )


class CreatePasswordViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Participant.objects

    def create(self, request, *args, **kwargs):
        password = request.data.get('newPassword', None)
        token = request.data.get('token', None)
        participant = None

        if token and password:
            participant = self.queryset.filter(
                tokens__token=token,
                tokens__token_type=PASSWORD_RESET,
                tokens__used=False,
                tokens__valid_until__gt=localtime(now()),
            ).first()

        if participant and password:
            serializer = ParticipantPasswordSerializer(
                participant,
                {'password': password},
            )
            serializer.is_valid(raise_exception=True)
            participant.tokens\
                .filter(token_type=PASSWORD_RESET)\
                .update(used=True)
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {
                'errors': [
                    'invalid-token',
                ],
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )
