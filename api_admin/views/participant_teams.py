from api.models import Team, Year
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.shortcuts import render


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
        .order_by('-count')
    return render(
        request,
        'stats/participant_teams.html',
        {
            'festival': festival,
            'teams': teams,
        },
    )
