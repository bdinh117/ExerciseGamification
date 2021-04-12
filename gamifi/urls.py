from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'gamifi'

urlpatterns = [
    path("", views.home, name="home"),
    path('profile/', views.profile,name="profile"),
    path('editprofile/', views.edit_profile,name="edit-profile"),
    path('send_friend_request/<int:userID>/',views.send_friend_request, name='send friend request'),
    path('accept_friend_request/<int:userID>/',views.accept_friend_request, name='accept friend request'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)