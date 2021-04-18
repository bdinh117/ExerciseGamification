from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import (AerobicCreateView, AerobicUpdateView, StrengthCreateView, StrengthUpdateView,
                    FlexibilityCreateView,FlexibilityUpdateView,LeaderboardListView, UserFriendsListView)
from django.views.generic import TemplateView
app_name = 'gamifi'

urlpatterns = [
    path("", views.home, name="home"),
    path('activity_log/',views.activity_log,name="activity-log"),
    path('leaderboard/',LeaderboardListView.as_view(),name='leaderboard'),
    path('profile/<str:username>/', views.profile,name='profile'),
    path('editprofile/', views.edit_profile,name="edit-profile"),
    path('friends/',UserFriendsListView.as_view(),name='friends-list'),
    path('send_friend_request/<int:pk>',views.send_friend_request,name="send-friend-request"),
    path('accept_friend_request/<int:pk>',views.accept_friend_request,name="accept-friend-request"),
    path('exercise/new/',TemplateView.as_view(template_name="gamifi/choose_exercise.html"),name= 'exercise-create'),
    path('exercise/Aerobic/new/', AerobicCreateView.as_view(), name='aerobic-create'),
    path('exercise/Strength/new/', StrengthCreateView.as_view(), name='strength-create'),
    path('exercise/Flexibility/new/', FlexibilityCreateView.as_view(), name='flexibility-create'),
    path('exercise/Aerobic/update/<int:pk>/', AerobicUpdateView.as_view(), name='aerobic-update'),
    path('exercise/Strength/update/<int:pk>/', StrengthUpdateView.as_view(), name='strength-update'),
    path('exercise/Flexibility/update/<int:pk>/', FlexibilityUpdateView.as_view(), name='flexibility-update'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)