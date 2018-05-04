from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

from api.models import Participant, Team, Year


@staff_member_required
def participant_teams(request, festivalId):
    festival = Year.objects.get(pk=festivalId)
    teams = Team.objects\
        .filter(
            participant__orders__year=festivalId,
            participant__orders__paid=True,
            participant__orders__canceled=False,
        )\
        .annotate(count=Count('participant'))\
        .order_by('-count')\
        .all()

    data = [team for team in teams]
    teamless_count = Participant.objects.filter(
        team=None,
        orders__year=festivalId,
        orders__paid=True,
        orders__canceled=False,
    ).distinct().count()
    data.append({
        'name': _('None'),
        'count': teamless_count,
    })
    return render(
        request,
        'stats/participant_teams.html',
        {
            'festival': festival,
            'teams': data,
        },
    )
