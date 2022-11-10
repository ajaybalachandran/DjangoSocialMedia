from django.shortcuts import render, redirect
from django.views.generic import View, CreateView, FormView, TemplateView, ListView
from socialapp.forms import RegistrationForm, LoginForm, ProfileForm, ProfilePicChangeForm
from socialapp.models import Myuser, Posts, UserProfile, Comments
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

# Create your views here.
def signin_required(fn):
  def wrapper(request, *args, **kwargs):
    if not request.user.is_authenticated:
      return redirect('social-login')
    else:
      return fn(request, *args, **kwargs)
  return wrapper

decs = [signin_required, never_cache]

@method_decorator(decs, name='dispatch')
class HomeView(View):
  def get(self, request, *args, **kwargs):
    # posts = Posts.objects.all().exclude(user=self.request.user)
    posts = Posts.objects.all()
    if posts:
      return render(request, 'index.html', {'allposts': posts})
    else:
      return render(request, 'index.html')

class RegistrationView(CreateView):
  model = Myuser
  form_class = RegistrationForm
  template_name = 'signup.html'
  success_url = reverse_lazy('social-login')
  
  # def form_valid(self, form):
  #   form.instance.profile_pic = self.request.FILES['profile_pic']
  #   return super().form_valid(form)


class LoginView(FormView):
  form_class = LoginForm
  template_name = 'login.html'
  
  def post(self, request, *args, **kwargs):
    form = LoginForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password')
      usr = authenticate(request, username=username, password=password)
      if usr:
        login(request, usr)
        return redirect('social-home')
      else:
        return redirect('social-login')


decs
def signout_view(request,  *args, **kwargs):
  logout(request)
  return redirect('social-login')


@method_decorator(decs, name='dispatch')
class PostsView(View):
  def get(self, request, *args, **kwargs):
    return render(request, 'newpost.html')

  def post(self, request, *args, **kwargs):
    title = request.POST.get('title')
    description = request.POST.get('description')
    post_image = request.FILES['post_image']
    Posts.objects.create(title=title, description=description, 
    post_image=post_image, user=request.user)
    return redirect('social-home')


# class PostListView(ListView):
#   template_name = 'index.html'
#   model = Posts
#   context_object_name = 'allposts'


@method_decorator(decs, name='dispatch')
class MyProfileView(View):
  def get(self, request, *args, **kwargs):
    posts = request.user.my_post.all()
    return render(request, 'profile.html', {'myposts': posts})


@method_decorator(decs, name='dispatch')
class AddProfileView(CreateView):
  model = UserProfile
  form_class = ProfileForm
  template_name = 'profile_add_edit.html'
  success_url = reverse_lazy('social-my-profile')

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)


@method_decorator(decs, name='dispatch')
class ProfileEditView(View):
  def get(self, request, *args, **kwargs):
    data = UserProfile.objects.get(user=request.user)
    form = ProfileForm(instance=data)
    return render(request, 'profile_add_edit.html', {'form': form})

  def post(self, request, *args, **kwargs):
    profile = UserProfile.objects.get(user=request.user)
    form = ProfileForm(request.POST, instance=profile)
    if form.is_valid():
      form.save()
      return redirect('social-my-profile')


@method_decorator(decs, name='dispatch')
class ChangeProfilePicView(View):
  def get(self, request):
        return render(request, 'profile.html')

  def post(self, request):
    form = ProfilePicChangeForm(request.POST, request.FILES, instance=request.user)
    if form.is_valid():
      form.save()
      return redirect('social-my-profile')



decs
def add_comment_view(request, *args, **kwargs):
  if request.method == 'POST':
    post_id = kwargs.get('id')
    post = Posts.objects.get(id=post_id)
    comment = request.POST.get('comment')
    Comments.objects.create(post=post, user=request.user, comment=comment)
    return redirect('social-home')
  else:
    return redirect('social-home')


decs
@login_required
def add_like_view(request, *args, **kwargs):
  if request.method == 'POST':
    id = kwargs.get('id')
    post = Posts.objects.get(id=id)
    if request.user not in post.liked_by.all():
      post.liked_by.add(request.user)
    else:
      post.liked_by.remove(request.user)
    return redirect('social-home')


decs
@login_required
def others_profile_view(request, *args, **kwargs):
  id = kwargs.get('id')
  user = Myuser.objects.get(id=id)
  posts = user.my_post.all()
  return render(request, 'other-profile.html', {'other_user': user, 'otherposts': posts})
      

@method_decorator(decs, name='dispatch')
class FollowView(View):
  def post(self, request, *args, **kwargs):
    id = kwargs.get('id')
    # here other_user is the user who is going to followed by the request.useryyyyy
    other_user = Myuser.objects.get(id=id)
    # other_user_profile = UserProfile.objects.get(user=other_user)
    other_user_profile = other_user.user_profile
    other_user_profile.followers.add(request.user)
    other_user_profile.save()

    user_profile = request.user.user_profile
    user_profile.following.add(other_user)
    user_profile.save()
    posts = other_user.my_post.all()
    return render(request, 'other-profile.html', {'other_user': other_user, 'otherposts': posts})


class UnfollowView(View):
  def post(self, request, *args, **kwargs):
    id = kwargs.get('id')
    other_user = Myuser.objects.get(id=id)
    other_user_profile = other_user.user_profile
    other_user_profile.followers.remove(request.user)
    other_user_profile.save()

    user_profile = request.user.user_profile
    user_profile.following.remove(other_user)
    user_profile.save()
    posts = other_user.my_post.all()
    return render(request, 'other-profile.html', {'other_user': other_user, 'otherposts': posts})



