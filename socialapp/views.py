from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, FormView, ListView, DetailView, DeleteView,UpdateView
from socialapp.forms import RegistrationForm, LoginForm, PostForm, CommentForm
from socialapp.models import Myuser, Comment, Posts, Profile
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache


# Create your views here.
def signin_required(fn):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # messages.error("you must log in")
            return redirect("signin")
        else:
            return fn(request, *args, **kwargs)
    return wrapper
decs = [signin_required, never_cache]


class SignupView(CreateView):
    model = Myuser
    form_class = RegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy("signin")


class LoginView(FormView):
    template_name = "login.html"
    form_class = LoginForm

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get("username")
            pswd = form.cleaned_data.get("password")
            usr = authenticate(request, username=uname, password=pswd)
            if usr:
                login(request, usr)
                return redirect("index")
            else:
                return render(request, self.template_name, {"form": form})


@method_decorator(decs, name="dispatch")
class IndexView(ListView):
    template_name = "home.html"
    model = Posts
    context_object_name = "posts"
    success_url = reverse_lazy("index")
    form_class=CommentForm
    


    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        form =CommentForm()
        context["cform"]=form
        comment=Comment.objects.all()
        context["comment"]=comment
        users=Myuser.objects.all().exclude(username=self.request.user)
        context['users']=users
        return context
  
    

@method_decorator(decs, name="dispatch")
class NewPostView(CreateView):
    template_name = 'newpost.html'
    form_class = PostForm
    model = Posts
    context_object_name = "posts"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        form.instance.user = self.request.user
        print("newpost")
        return super().form_valid(form)

@method_decorator(decs, name="dispatch")
class FeedsView(ListView):
    model = Posts
    template_name = "feeds.html"
    context_object_name = "posts"

@method_decorator(decs, name="dispatch")
class CommentFormView(CreateView):
    template_name = "home.html"
    form_class = CommentForm
    model = Comment
    success_url = "index"
    pk_url_kwarg="id"
    

    def form_valid(self, form):
        form.instance.user=self.request.user
        print("comment added")
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form=CommentForm(request.POST)
        if form.is_valid():
            pos_id=kwargs.get('id')  
            comment=form.cleaned_data.get("comment")
            user=self.request.user
            post=Posts.objects.get(id=pos_id)
            Comment.objects.create(comment=comment,user=user,post=post)   
            print("new comment added")                        
            return redirect("index")            
        else:
            return redirect("index")


@method_decorator(decs, name="dispatch")            
class CommentListView(ListView):
    model=Comment
    context_object_name="allcomments"
    template_name="home.html"

@method_decorator(decs, name="dispatch")    
class ProfileView(ListView):
    template_name = "profile.html"
    model = Profile
    context_object_name = "profile"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)

        id=self.kwargs.get("id")
        print(id)
        if id is None:
            
            prof = Profile.objects.filter(user=self.request.user)
            context['User'] = prof
        else:
            user=Myuser.objects.get(id=id)
            print(user)
            prof = Profile.objects.filter(user=user)
            context['User'] = user
            print(prof)



        # # Get the profiles from the QuerySet
    

        # Add the profiles to the context
        context['profiles'] = prof

        # Iterate over the profiles in the QuerySet
        for p in prof:
            # Get the number of followers for the profile
            num_followers = p.followers.count()
            context["followers"] = num_followers

            # Get the number of profiles the user is following
            num_following = p.following.count()
            context["following"] = num_following
            

        return context

# To update the profile
@method_decorator(decs, name="dispatch")
class ProfileUpdateView(UpdateView):
    template_name="updateprofile.html"
    form_class=RegistrationForm
    model=Myuser
    pk_url_kwarg="id"
    success_url=reverse_lazy("profile")


class UserView(ListView):
    templatename="home.html"
    model=Myuser
    context_object_name="users"

def userprofileview(request, *args, **kwargs):
    id=kwargs.get("id")
    user=Myuser.objects.get(id=id)
    post=Posts.objects.filter(user_id=id)
    comments=Comment.objects.all()
    return render(request,"userprofile.html",{'post':post, 'user':user,'comments':comments})


def signout_view(request, *args, **kwargs):
    logout(request)
    messages.success(request, "you logout successfully")
    print("signout successfully")
    return redirect("signin")

def add_likes(request, *args, **kwargs):
    p_id=kwargs.get("id")
    pos=Posts.objects.get(id=p_id)
    pos.num_likes.add(request.user)
    pos.save()
    print("likes added")
    return redirect("index")

def remove_likes(request, *args, **kwargs):
    pos_id=kwargs.get("id")
    pos=Posts.objects.get(id=pos_id)
    pos.num_likes.remove(request.user)
    pos.save()
    print("likes removed")
    return redirect("index")
    