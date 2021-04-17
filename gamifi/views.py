
# Create your views here.

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.db.models import Sum

from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Goal, AerobicExercise, StrengthExercise, FlexibilityExercise, Exercise, User, Profile
from .forms import UserUpdateForm, ProfileUpdateForm, GoalUpdateForm, AerobicExerciseForm, StrengthExerciseForm, FlexibilityExerciseForm
from itertools import chain


def home(request):
    return render(request, 'gamifi/index.html')

@login_required
def activity_log(request):
    #For every exercise completed, sum up exp
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
def profile(request):
    context = {
        'goals': Goal.objects.filter(user=request.user)
    }
    return render(request, 'gamifi/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
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
