from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import ExerciseCreateView, ExerciseUpdateView, ExerciseDetailView

app_name = 'gamifi'

urlpatterns = [
    path("", views.home, name="home"),
    path('exercise/<int:pk>/', ExerciseDetailView.as_view(), name='exercise-detail'),
    path('exercise/<int:pk>/update/', ExerciseUpdateView.as_view(), name='exercise-update'),
    path('profile/', views.profile,name="profile"),
    path('editprofile/', views.edit_profile,name="edit-profile"),
    path('exercise/new/', ExerciseCreateView.as_view(), name='exercise-create'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)