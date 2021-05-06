from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import (LeaderboardListView, UserFriendsListView,ExerciseChoiceDetailView,ExerciseCreateView,ExerciseUpdateView)
from django.views.generic import TemplateView
app_name = 'gamifi'


urlpatterns = [
    path("", views.home, name="home"),
    path('activity_log/',views.activity_log,name="activity-log"),
    path('leaderboard/',LeaderboardListView.as_view(),name='leaderboard'),
    path('profile/<str:username>/', views.profile,name='profile'),
    path('editprofile/', views.edit_profile,name="edit-profile"),
    path('friends/',UserFriendsListView.as_view(),name='friends-list'),
    path('send_friend_request/<int:pk>/',views.send_friend_request,name="send-friend-request"),
    path('accept_friend_request/<int:pk>/',views.accept_friend_request,name="accept-friend-request"),
    path('deny_friend_request/<int:pk>/',views.deny_friend_request,name="deny-friend-request"),
    path('unfriend/<str:username>/',views.unfriend,name="unfriend"),
    path('catalog/',views.catalog,name= 'exercise-catalog'),
    path('exercise/<int:pk>/',ExerciseChoiceDetailView.as_view(),name= 'exercise-detail'),
    path('exercise/new/',ExerciseCreateView.as_view(),name= 'exercise-create'),
    path('exercise/new/<str:name>_<str:type>/',ExerciseCreateView.as_view(),name= 'exercise-create-preset'),
    path('exercise/update/<int:pk>/', ExerciseUpdateView.as_view(), name='exercise-update'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
