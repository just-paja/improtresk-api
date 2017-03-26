from django.http import HttpResponseForbidden

from datetime import datetime, timedelta

from rest_framework import mixins, serializers, viewsets

from rest_framework_extensions.mixins import NestedViewSetMixin

from .performers import PerformerSerializer
from .. import models


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class PollVoteSerializer(serializers.ModelSerializer):
    remoteAddr = serializers.CharField(
        source='remote_addr',
        required=False,
    )

    class Meta:
        model = models.PollVote
        fields = (
            'id',
            'answer',
            'remoteAddr',
        )

    def create(self, validated_data, *args, **kwargs):
        return super().create({
            'answer': validated_data['answer'],
            'remote_addr': get_client_ip(self.context['request']),
        }, *args, **kwargs)


class PollAnswerSerializer(serializers.ModelSerializer):
    answerCount = serializers.IntegerField(source='get_vote_count')
    createdAt = serializers.DateTimeField(source='created_at')
    updatedAt = serializers.DateTimeField(source='updated_at')
    performer = PerformerSerializer(many=False)

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
    answerCount = serializers.IntegerField(source='get_vote_count')
    createdAt = serializers.DateTimeField(source='created_at')
    updatedAt = serializers.DateTimeField(source='updated_at')

    class Meta:
        model = models.Poll
        fields = (
            'answerCount',
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

    def create(self, request, *args, **kwargs):
        similar_votes = models.PollVote.objects\
            .filter(
                answer__poll=kwargs['parent_lookup_answer__poll'],
                remote_addr=get_client_ip(request),
                created_at__gt=datetime.now() - timedelta(hours=1),
            )\
            .count()

        if similar_votes > 0:
            return HttpResponseForbidden()

        return super().create(request, *args, **kwargs)
