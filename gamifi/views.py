
# Create your views here.

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.db.models import Sum

from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Goal, Exercise
from .forms import UserUpdateForm, ProfileUpdateForm, GoalUpdateForm, ExerciseForm

def home(request):
    exp_total=Exercise.objects.filter(user=request.user, finished=True).aggregate(Sum('exp'))
    context = {
        'exercise_list': Exercise.objects.filter(user=request.user),
        'exp_total': exp_total['exp__sum']
    }
    return render(request, 'gamifi/index.html',context)

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

class ExerciseDetailView(generic.DetailView):
    model = Exercise

class ExerciseCreateView(generic.CreateView):
    form_class = ExerciseForm
    template_name = 'gamifi/exercise_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ExerciseUpdateView(generic.UpdateView):
    model = Exercise
    form_class = ExerciseForm
    template_name = 'gamifi/exercise_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ExerciseListView(generic.ListView):
    model= Exercise
    template_name = 'gamifi/index.html'

    def get_queryset(self):#filter what objects to get a list of
        return Exercise.objects.filter(user=self.request.user)#only get the user's own Exercises.

