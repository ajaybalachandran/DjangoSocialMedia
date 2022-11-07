from django.shortcuts import render, redirect
from django.views.generic import View, CreateView, FormView, TemplateView
from socialapp.forms import RegistrationForm, LoginForm
from socialapp.models import Myuser, Posts
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
class HomeView(TemplateView):
  template_name = 'index.html'

class RegistrationView(CreateView):
  model = Myuser
  form_class = RegistrationForm
  template_name = 'signup.html'
  success_url = reverse_lazy('social-login')


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
    post_image = request.POST.get('post_image')
    Posts.objects.create(title=title, description=description, 
    post_image=post_image, user=request.user)
    return redirect('social-home')
