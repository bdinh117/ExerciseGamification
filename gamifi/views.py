
# Create your views here.

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.db.models import Sum

from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Exercise, User, Profile, FriendRequest, ExerciseChoice
from .forms import UserUpdateForm, ProfileUpdateForm, CommentForm, ExerciseForm
from itertools import chain
from django.contrib import messages
import requests
import re

def home(request):
    return render(request, 'gamifi/index.html')

@login_required
def catalog(request):
    #REFERENCED THIS SOURCE:  https://dev.to/yahaya_hk/how-to-populate-your-database-with-data-from-an-external-api-in-django-398i
    if (ExerciseChoice.objects.count()==0):
        url ="https://wger.de/api/v2/exerciseinfo/"
        PARAMS ={'language':'2','limit':'300'}
        headers = {'Accept': 'application/json','Authorization': 'Token ***REMOVED***'}
        response = requests.get(url=url,headers=headers,params=PARAMS)
        exercises = response.json()["results"]

        #regex for filtering out html tags
        cleanr = re.compile('<.*?>')

        for e in exercises:
            desc = re.sub(cleanr, '', e['description'])
            if (len(e['images']) > 0):
                exercise_data = ExerciseChoice(
                    name=e['name'],
                    description=desc,
                    category=e['category']['name'],
                    image_url=e['images'][0]['image']
                )
            else:
                exercise_data = ExerciseChoice(
                    name=e['name'],
                    description=desc,
                    category=e['category']['name'],
                )

            exercise_data.save()

    all_exercises=ExerciseChoice.objects.all()
    context = {'exercises':all_exercises}
    return render(request,'gamifi/catalog.html',context)

class ExerciseChoiceDetailView(generic.DetailView):
    model = ExerciseChoice
    template_name = 'gamifi/exercise_detail.html'

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


#https://medium.com/analytics-vidhya/add-friends-with-689a2fa4e41d , referenced for friend requests
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

@login_required
def deny_friend_request(request,pk):
    friend_request=FriendRequest.objects.get(pk=pk)
    if friend_request.receiver == request.user:
        friend_request.delete()
        messages.success(request, "friend request denied!")
        return redirect('gamifi:profile',username=request.user.username)
    else:
        return HttpResponse('---------------')

@login_required
def unfriend(request,username):
   ex_friend=User.objects.get(username=username)

   #sever the bond. :(
   request.user.profile.friends.remove(ex_friend)
   ex_friend.profile.friends.remove(request.user)
   return redirect('gamifi:friends-list')

class UserFriendsListView(generic.ListView):
    model = User
    template_name = "gamifi/friends_list.html"

    def get_queryset(self):
        return self.request.user.profile.friends.all() #get all of the user's friends, in object_list
        #return User.objects.filter(profile__friends=self.request.user)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the friend requests sent to this user
        context['all_friend_requests'] = FriendRequest.objects.filter(receiver=self.request.user)
        return context

@login_required
def activity_log(request):
    #For every completed exercise, sum up exp
    exercise_total = Exercise.objects.filter(user=request.user, finished=True).aggregate(Sum('exp'))['exp__sum']

    #update exp total for user
    exp_total=sum(filter(None,[exercise_total]))
    Profile.objects.filter(user=request.user).update(experience=exp_total)

    exercise_list=Exercise.objects.filter(user=request.user)

    context = {'exercise_list':exercise_list,
               'exp_total':exp_total}
    return render(request, 'gamifi/activity_log.html',context)



#https://www.youtube.com/watch?v=UmljXZIypDc&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p, refereneced Corey Schafer django tutorial series for profile makign
@login_required
def profile(request,username):
    # 'usr' is who the profile being viewed belongs to. "user" in the template is the person viewing the page
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

class ExerciseCreateView(generic.CreateView):
    form_class = ExerciseForm
    template_name = 'gamifi/exercise_form.html'

    #Prepopulate form with url parameters if given
    def get_initial(self):
        initial = super().get_initial()
        if('name' in self.kwargs and 'type' in self.kwargs):
            initial['name'] = self.kwargs['name']
            initial['category'] = self.kwargs['type']
        return initial

    def form_valid(self, form):
        #form=form(initial={'name': self.kwargs['name']})
        form.instance.user = self.request.user
        return super().form_valid(form)

class ExerciseUpdateView(generic.UpdateView):
    model = Exercise
    form_class = ExerciseForm
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
