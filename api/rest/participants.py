from datetime import date

from rest_framework import permissions, serializers, status, validators, viewsets

from rest_framework.response import Response

from rest_framework_extensions.mixins import NestedViewSetMixin

from ..models import Participant, Team


def is_true(value):
    if not value:
        raise serializers.ValidationError('Field is required')


def is_eighteen(value):
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))

    if age < 18:
        raise serializers.ValidationError('Must be older than 18 years')


class ParticipantSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[
            validators.UniqueValidator(
                queryset=Participant.objects.all(),
            ),
        ],
    )
    birthday = serializers.DateField(
        validators=[is_eighteen],
    )
    rules_accepted = serializers.BooleanField(
        validators=[is_true],
    )

    class Meta:
        model = Participant
        fields = (
            'id',
            'name',
            'address',
            'team',
            'email',
            'phone',
            'birthday',
            'rules_accepted',
            'newsletter',
            'paid',
            'assigned_workshop',
        )


class ParticipantViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = [permissions.IsAdminUser]


class RegisterViewSet(viewsets.ViewSet):
    def create(self, request):
        data = request.data.copy()
        team = None
        team_name = data.get('team_name', None)

        if team_name:
            try:
                team = Team.objects.get(name=team_name)
            except Team.DoesNotExist:
                team = Team.objects.create(name=team_name)

        if team:
            data['team'] = team.id

        serializer = ParticipantSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
