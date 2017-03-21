from rest_framework import mixins, serializers, viewsets

from rest_framework_extensions.mixins import NestedViewSetMixin

from .. import models


class PollVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PollVote
        fields = (
            'id',
            'answer',
        )


class PollAnswerSerializer(serializers.ModelSerializer):
    answerCount = serializers.IntegerField(source='get_vote_count')
    createdAt = serializers.DateTimeField(source='created_at')
    updatedAt = serializers.DateTimeField(source='updated_at')

    class Meta:
        model = models.PollAnswer
        fields = (
            'answerCount',
            'createdAt',
            'id',
            'performer',
            'poll',
            'text',
            'updatedAt',
        )


class PollSerializer(serializers.ModelSerializer):
    answers = PollAnswerSerializer(many=True)
    createdAt = serializers.DateTimeField(source='created_at')
    updatedAt = serializers.DateTimeField(source='updated_at')

    class Meta:
        model = models.Poll
        fields = (
            'answers',
            'closed',
            'createdAt',
            'id',
            'question',
            'updatedAt',
        )


class PollViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Poll.objects.all()
    serializer_class = PollSerializer


class PollVoteViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
    NestedViewSetMixin,
):
    queryset = models.PollVote.objects.all()
    serializer_class = PollVoteSerializer
