
# Create your views here.

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.db.models import Sum

from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import AerobicExercise, StrengthExercise, FlexibilityExercise, Exercise, User, Profile, FriendRequest
from .forms import UserUpdateForm, ProfileUpdateForm, AerobicExerciseForm, StrengthExerciseForm, FlexibilityExerciseForm, CommentForm
from itertools import chain
from django.contrib import messages
import requests
import json

def get_exercises(request):
    url ="https://wger.de/api/v2/exercise/"
    PARAMS ={'language':'2','limit':'300'}
    headers = {'Accept': 'application/json','Authorization': 'Token ***REMOVED***'}
    response = requests.get(url=url,headers=headers,params=PARAMS)
    exercises = response.json()["results"]
    context = {'exercises':exercises}
    return render(request,'gamifi/catalog.html',context)


def home(request):
    return render(request, 'gamifi/index.html')

@login_required
def send_friend_request(request, pk):
    sender = request.user
    receiver = User.objects.get(pk=pk)
    friend_request, created = FriendRequest.objects.get_or_create(sender=sender, receiver=receiver)
    if created:
        #messages.success(request, "friend request sent!")
        return redirect('gamifi:profile',username=request.user.username)
    else:
        #messages.ERROR(request, "friend request was already sent")
        return HttpResponse("already sent")

@login_required
def accept_friend_request(request,pk):
    friend_request=FriendRequest.objects.get(pk=pk)
    if friend_request.receiver == request.user:
        friend_request.sender.profile.friends.add(request.user)
        friend_request.receiver.profile.friends.add(friend_request.sender)
        friend_request.delete()
        messages.success(request, "friend request accepted!")
        return redirect('gamifi:profile',username=request.user.username)
    else:
        return HttpResponse('friend request not accepted')

class UserFriendsListView(generic.ListView):
    model = User
    template_name = "gamifi/friends_list.html"

    def get_queryset(self):
        return self.request.user.profile.friends.all()
        #return User.objects.filter(profile__friends=self.request.user)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the friend requests that the user has been sent
        context['all_friend_requests'] = FriendRequest.objects.filter(receiver=self.request.user)
        return context

@login_required
def activity_log(request):
    #For every completed exercise, sum up exp
    aerobic_total=AerobicExercise.objects.filter(user=request.user, finished=True).aggregate(Sum('exp'))['exp__sum']
    strength_total = StrengthExercise.objects.filter(user=request.user, finished=True).aggregate(Sum('exp'))['exp__sum']
    flexibility_total= FlexibilityExercise.objects.filter(user=request.user, finished=True).aggregate(Sum('exp'))['exp__sum']

    #update exp total for user
    exp_total=sum(filter(None,[aerobic_total,strength_total,flexibility_total]))
    Profile.objects.filter(user=request.user).update(experience=exp_total)

    #pass exercises into template
    aerobic_list=AerobicExercise.objects.filter(user=request.user)
    strength_list= StrengthExercise.objects.filter(user=request.user)
    flexibility_list= FlexibilityExercise.objects.filter(user=request.user)
    exercise_list=list(chain(aerobic_list, strength_list, flexibility_list))

    context = {
        'exercise_list': exercise_list,
        'exp_total': exp_total
    }

    return render(request, 'gamifi/activity_log.html',context)

@login_required
def profile(request,username):
    # the user of the profile being viewed. "user" in the template is the person viewing the page
    usr = User.objects.get(username=username)
    #handle commenting
    if request.method == 'POST':
        c_form = CommentForm(data=request.POST)
        if c_form.is_valid():
            new_comment= c_form.save(commit=False) #get the new comment
            new_comment.profile = usr.profile #tie it to the profile being commented on
            new_comment.save()
            return redirect('gamifi:profile',username=username)
    else:
        c_form=CommentForm()
    context = {
        'usr':usr,
        'friends': request.user.profile.friends.all(), #pass in a list of friends for the purpose of deciding what buttons appear on the page
        'c_form': c_form,
        'comments':usr.profile.comment_set.all()
    }
    return render(request, 'gamifi/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('gamifi:profile',username=request.user.username)

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'gamifi/edit_profile.html', context)


class AerobicCreateView(generic.CreateView):
    form_class = AerobicExerciseForm
    template_name = 'gamifi/exercise_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AerobicUpdateView(generic.UpdateView):
    model = AerobicExercise
    form_class = AerobicExerciseForm
    template_name = 'gamifi/exercise_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class StrengthCreateView(generic.CreateView):
    form_class = StrengthExerciseForm
    template_name = 'gamifi/exercise_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class StrengthUpdateView(generic.UpdateView):
    model = StrengthExercise
    form_class = StrengthExerciseForm
    template_name = 'gamifi/exercise_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class FlexibilityCreateView(generic.CreateView):
    form_class = FlexibilityExerciseForm
    template_name = 'gamifi/exercise_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class FlexibilityUpdateView(generic.UpdateView):
    model = FlexibilityExercise
    form_class = FlexibilityExerciseForm
    template_name = 'gamifi/exercise_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class LeaderboardListView(generic.ListView):
    model= User
    template_name = 'gamifi/leaderboard_list.html'
    #context_object_name is object_list
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        #return list of users with their total exp in their profile. pass it into context
        leaders = User.objects.annotate(total=Sum('profile__experience')).order_by('-total')
        context['user_list'] = leaders
        return context
