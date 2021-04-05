
# Create your views here.

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Goal


def home(request):
    return render(request, 'gamifi/index.html')

@login_required
def profile(request):
    context = {
        'goals': Goal.objects.filter(user=request.user)
    }
    return render(request, 'gamifi/profile.html', context)

