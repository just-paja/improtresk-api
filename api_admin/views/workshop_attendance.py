from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .workshop_participants import get_workshop_participants_data


@staff_member_required
def workshop_attendance(request, festivalId):
    return render(
        request,
        'stats/workshop_attendants.html',
        get_workshop_participants_data(festivalId),
    )
