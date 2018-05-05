from datetime import date

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.timezone import localtime, now
from django.http import Http404

from rest_framework import mixins, permissions, serializers, status, viewsets

from rest_framework.response import Response

from ..models import Participant
from ..models.participantToken import PASSWORD_RESET


def is_true(value):
    if not value:
        raise serializers.ValidationError('forms.errors.must-accept-rules')


def is_eighteen(value):
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))

    if age < 18:
        raise serializers.ValidationError('forms.errors.must-be-eighteen')


class ParticipantUpdateSerializer(serializers.HyperlinkedModelSerializer):
    team_name = serializers.CharField(
        write_only=True,
        allow_blank=True,
        required=False,
    )
    team = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='name',
    )
    idNumber = serializers.CharField(source='id_number')
    email = serializers.EmailField()

    class Meta:
        model = Participant
        fields = (
            'address',
            'email',
            'id',
            'idNumber',
            'name',
            'phone',
            'team_name',
            'team',
        )

    def to_internal_value(self, data):
        internal_value = super(ParticipantUpdateSerializer, self).to_internal_value(data)
        email = data.get('email', None)
        if email:
            internal_value.update({
                "email": data.get("email")
            })
        return internal_value

    def validate_email(self, value):
        participant_exists = Participant.objects.filter(email=value)
        user_exists = User.objects.filter(email=value)
        if self.instance:
            participant_exists = participant_exists.exclude(pk=self.instance.pk)
            user_exists = user_exists.exclude(pk=self.user.pk)
        if participant_exists or user_exists:
            raise ValidationError("forms.errors.email-already-exists")

    def create(self, validated_data):
        validated_data['username'] = validated_data['email']
        participant = super().create(validated_data)
        participant.set_password(validated_data['password'])
        participant.save()
        return participant

    def set_user(self, user):
        self.user = user


class ParticipantSerializer(ParticipantUpdateSerializer):
    birthday = serializers.DateField(
        validators=[is_eighteen],
    )
    rules_accepted = serializers.BooleanField(
        validators=[is_true],
    )
    assignments = serializers.SlugRelatedField(
        source="workshops",
        many=True,
        read_only=True,
        slug_field='workshop_id',
    )
    idNumber = serializers.CharField(
        source='id_number',
        required=False,
    )

    class Meta:
        model = Participant
        fields = (
            'address',
            'id',
            'idNumber',
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
            'assignments',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }


class ParticipantPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ('password',)
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class ParticipantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = [permissions.IsAdminUser]


class RegistrationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer


class WhoAmIViewSet(viewsets.GenericViewSet):
    queryset = Participant.objects
    serializer_class = ParticipantUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'patch', 'head', 'options']

    def get_serializer_class(self):
        if self.action == 'list':
            return ParticipantSerializer
        return ParticipantUpdateSerializer

    def list(self, request):
        try:
            participant = request.user.participant
        except ObjectDoesNotExist:
            raise Http404
        serializer = self.get_serializer(participant)
        return Response(serializer.data)

    def patch(self, request):
        try:
            participant = request.user.participant
        except ObjectDoesNotExist:
            raise Http404
        serializer = self.get_serializer(data=request.data, instance=participant, partial=True)
        serializer.set_user(request.user)
        if serializer.is_valid():
            serializer.save()
            response_serializer = ParticipantSerializer(participant)
            return Response(response_serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


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
            status=status.HTTP_400_BAD_REQUEST,
        )


class ChangePasswordViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    def create(self, request, *args, **kwargs):
        try:
            participant = request.user.participant
        except ObjectDoesNotExist:
            raise Http404

        password = request.data.get('newPassword', None)
        serializer = ParticipantPasswordSerializer(
            participant,
            {'password': password},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
