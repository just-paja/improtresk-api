from api.models import Year
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render


@staff_member_required
def index(request):
    festivals = Year.objects.all()
    return render(request, 'stats/index.html', {'festivals': festivals})
