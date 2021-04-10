from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import ExerciseCreateView, ExerciseListView

app_name = 'gamifi'

urlpatterns = [
    path("", ExerciseListView.as_view(), name="home"),
    path('profile/', views.profile,name="profile"),
    path('editprofile/', views.edit_profile,name="edit-profile"),
    path('AddExercise/', ExerciseCreateView.as_view(), name='exercise-create'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)