
# Create your views here.

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.db.models import Sum

from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Goal, AerobicExercise, StrengthExercise, FlexibilityExercise, Exercise, User
from .forms import UserUpdateForm, ProfileUpdateForm, GoalUpdateForm, AerobicExerciseForm, StrengthExerciseForm, FlexibilityExerciseForm
from itertools import chain
from django.forms import inlineformset_factory


def home(request):
    return render(request, 'gamifi/index.html')

@login_required
def activity_log(request):
    aerobic_total=AerobicExercise.objects.filter(user=request.user, finished=True).aggregate(Sum('exp'))['exp__sum']
    strength_total = StrengthExercise.objects.filter(user=request.user, finished=True).aggregate(Sum('exp'))['exp__sum']
    flexibility_total= FlexibilityExercise.objects.filter(user=request.user, finished=True).aggregate(Sum('exp'))['exp__sum']

    exp_total=sum(filter(None,[aerobic_total,strength_total,flexibility_total]))

    aerobic_list=AerobicExercise.objects.filter(user=request.user)
    strength_list= StrengthExercise.objects.filter(user=request.user)
    flexibility_list= FlexibilityExercise.objects.filter(user=request.user)
    exercise_list=list(chain(aerobic_list, strength_list, flexibility_list))
    # AerobicFormSet = inlineformset_factory(User,AerobicExercise, fields=('finished',))
    # StrengthFormSet = inlineformset_factory(User,StrengthExercise, fields=('finished',))
    # FlexibilityFormSet = inlineformset_factory(User,FlexibilityExercise, fields=('finished',))
    # if request.method == 'POST':
    #     a_formset=AerobicFormSet(request.POST,instance=request.user)
    #     s_formset = StrengthFormSet(request.POST, instance=request.user)
    #     f_formset = FlexibilityFormSet(request.POST, instance=request.user)
    #
    #     if a_formset.is_valid() and s_formset.is_valid() and f_formset.is_valid():
    #         a_formset.save()
    #         s_formset.save()
    #         f_formset.save()
    #         return redirect('gamifi:home')
    #
    # else:
    #     a_formset = AerobicFormSet(instance=request.user)
    #     s_formset = StrengthFormSet( instance=request.user)
    #     f_formset = FlexibilityFormSet(instance=request.user)


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

# class ExerciseDetailView(generic.DetailView):
#     model = Exercise

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


# class ExerciseListView(generic.ListView):
#     model= Exercise
#     template_name = 'gamifi/index.html'
#
#     def get_queryset(self):#filter what objects to get a list of
#         return Exercise.objects.filter(user=self.request.user)#only get the user's own Exercises.

