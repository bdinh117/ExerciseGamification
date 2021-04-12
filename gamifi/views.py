
# Create your views here.

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic

from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Goal
from .forms import UserUpdateForm, ProfileUpdateForm, GoalUpdateForm
from django.contrib.auth.models import User

def home(request):
    return render(request, 'gamifi/index.html')

@login_required
def profile(request):
    profile = profile.objects.get(user=request.user)
    context = {
        'profile':profile,
        'goals': Goal.objects.filter(user=request.user)
    }
    return render(request, 'gamifi/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST': #
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if(not request.user.goal_set.exists()):
            request.user.goal_set.create()
        g_form = GoalUpdateForm(request.POST,instance=request.user.goal_set.first())
        if u_form.is_valid() and p_form.is_valid() and g_form.is_valid():
            u_form.save()
            p_form.save()
            g_form.save()
            return redirect('gamifi:profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        g_form = GoalUpdateForm(instance=request.user.goal_set.first())

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'g_form': g_form
    }

    return render(request, 'gamifi/edit_profile.html', context)

