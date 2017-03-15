from datetime import date

from django.core.exceptions import ValidationError

from rest_framework import mixins, permissions, serializers, viewsets

from rest_framework.response import Response

from rest_framework_extensions.mixins import NestedViewSetMixin

from ..models import Participant


def is_true(value):
    if not value:
        raise serializers.ValidationError('Rules must be accepted')


def is_eighteen(value):
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))

    if age < 18:
        raise serializers.ValidationError('Must be older than 18 years')


def is_email_unique(value):
    exists = Participant.objects.filter(email=value)
    if exists:
        raise ValidationError("Email address already exists, must be unique")


class ParticipantSerializer(serializers.HyperlinkedModelSerializer):
    team_name = serializers.CharField(
        write_only=True,
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
