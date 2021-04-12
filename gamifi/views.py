
# Create your views here.

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic

from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Profile, Goal, Friend_Request
from .forms import UserUpdateForm, ProfileUpdateForm, GoalUpdateForm

def home(request):
    return render(request, 'gamifi/index.html')

@login_required
def profile(request):
    context = {
        'goals': Goal.objects.filter(user=request.user)
    }
    return render(request, 'gamifi/profile.html', context)

@login_required
def send_friend_request(request,userID):
    from_user = request.user
    to_user = Profile.objects.get(id=userID)
    friend_request, created = Friend_Request.object.get_or_create(from_user=from_user,to_user=to_user)
    if created:
        return HttpResponse('friend request sent')
    else:
        return HttpResponse('friend request was already sent')
@login_required
def accept_friend_request(request,requestID):
    friend_request = Friend_Request.objects.get(id=requestID)
    if friend_request.to_user == request.user:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
        return HttpResponse('friend request was accepted')
    else:
        return HttpResponse('friend request not accepted')
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

