from django.shortcuts import render, redirect
from django.views.generic import View, CreateView, FormView, TemplateView, ListView
from socialapp.forms import RegistrationForm, LoginForm, ProfileForm, ProfilePicChangeForm
from socialapp.models import Myuser, Posts, UserProfile, Comments
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator

# Create your views here.
def signin_required(fn):
  def wrapper(request, *args, **kwargs):
    if not request.user.is_authenticated:
      return redirect('social-login')
    else:
      return fn(request, *args, **kwargs)
  return wrapper

@method_decorator(signin_required, name='dispatch')
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


def signout_view(request,  *args, **kwargs):
  logout(request)
  return redirect('social-login')


@method_decorator(signin_required, name='dispatch')
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


class MyProfileView(View):
  def get(self, request, *args, **kwargs):
    posts = request.user.my_post.all()
    return render(request, 'profile.html', {'myposts': posts})


class AddProfileView(CreateView):
  model = UserProfile
  form_class = ProfileForm
  template_name = 'profile_add_edit.html'
  success_url = reverse_lazy('social-my-profile')

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)


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


class ChangeProfilePicView(View):
  def get(self, request):
        return render(request, 'profile.html')

  def post(self, request):
    form = ProfilePicChangeForm(request.POST, request.FILES, instance=request.user)
    if form.is_valid():
      form.save()
      return redirect('social-my-profile')


def add_comment_view(request, *args, **kwargs):
  if request.method == 'POST':
    post_id = kwargs.get('id')
    post = Posts.objects.get(id=post_id)
    comment = request.POST.get('comment')
    Comments.objects.create(post=post, user=request.user, comment=comment)
    return redirect('social-home')
  else:
    return redirect('social-home')


def add_like_view(request, *args, **kwargs):
  if request.method == 'POST':
    id = kwargs.get('id')
    post = Posts.objects.get(id=id)
    if request.user not in post.liked_by.all():
      post.liked_by.add(request.user)
    else:
      post.liked_by.remove(request.user)
    return redirect('social-home')


def others_profile_view(request, *args, **kwargs):
  id = kwargs.get('id')
  user = Myuser.objects.get(id=id)
  posts = user.my_post.all()
  return render(request, 'other-profile.html', {'other_user': user, 'otherposts': posts})
      

@method_decorator(signin_required, name='dispatch')
class FollowView(View):
  def post(self, request, *args, **kwargs):
    id = kwargs.get('id')
    follow_user = Myuser.objects.get(id=id)
    follow_user_profile = UserProfile.objects.get(user=follow_user)
    follow_user_profile.followers.add(request.user)
    follow_user_profile.save()

    following_user_profile = request.user.user_profile
    following_user_profile.following.add(follow_user)
    following_user_profile.save()
    posts = follow_user.my_post.all()
    return render(request, 'other-profile.html', {'other_user': follow_user, 'otherposts': posts})



