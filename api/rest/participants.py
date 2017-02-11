from rest_framework import permissions, serializers, viewsets

from rest_framework_extensions.mixins import NestedViewSetMixin

from ..models import Participant


class ParticipantSerializer(serializers.HyperlinkedModelSerializer):
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

    class Meta:
        model = Participant
        fields = (
            'id',
            'name',
            'address',
            'team',
            'email',
            'phone',
            'rules_accepted',
            'newsletter',
            'paid',
            'assigned_workshop',
        )


class ParticipantViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = [permissions.IsAdminUser]
