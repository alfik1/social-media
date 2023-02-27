"""SocialApplication URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from socialapp import views

from django.urls import path
from django.conf import settings

from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("index",views.IndexView.as_view(),name="index"),
    path("register",views.SignupView.as_view(),name="register"),
    path("",views.LoginView.as_view(),name="signin"),
    path("newpost",views.NewPostView.as_view(),name="new-post"),
    path("index/like/<int:id>",views.add_likes,name="add-like"),
    path("index/unlike/<int:id>",views.remove_likes,name="unlike"),
    path("index/comment/<int:id>",views.CommentFormView.as_view(),name="comment"),
    path("feeds",views.FeedsView.as_view(),name="feeds"),
    path("profile",views.ProfileView.as_view(),name="profile"),
    path("profile/<int:id>",views.ProfileView.as_view(),name="profileview"),
    path("index/allusers/<int:id>",views.userprofileview,name="allusers"),
    path("index/profile/update/<int:id>",views.ProfileUpdateView.as_view(),name="profile-update"),
    path("logout",views.signout_view,name="signout"),
    
 ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
