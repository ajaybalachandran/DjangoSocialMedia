"""SocialMediaApplication URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from socialapp import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='social-home'),
    path('accounts/signup/', views.RegistrationView.as_view(), name='social-signup'),
    path('login/', views.LoginView.as_view(), name='social-login'),
    path('logout/', views.signout_view, name='social-logout'),
    path('newpost/', views.PostsView.as_view(), name='social-new-post'),
    path('profile/', views.MyProfileView.as_view(), name='social-my-profile'),
    path('user/myprofileadd/', views.AddProfileView.as_view(), name='social-add-profile'), 
    path('user/profileedit/', views.ProfileEditView.as_view(), name='social-edit-profile'),
    path('user/profilepic_change/', views.ChangeProfilePicView.as_view(), name='social-change-propic'), 
    path('posts/<int:id>/addcomment/', views.add_comment_view, name='social-add-comment'), 
    path('posts/<int:id>/like/', views.add_like_view, name='social-add-like'), 
    path('users/<int:id>/', views.others_profile_view, name='social-other-profile'), 
    path('users/<int:id>/follow/', views.FollowView.as_view(), name='social-follow'),
    path('users/<int:id>/unfollow/', views.UnfollowView.as_view(), name='social-unfollow')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)